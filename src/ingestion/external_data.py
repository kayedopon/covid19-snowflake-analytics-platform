from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pathlib import Path
from dotenv import load_dotenv


from country_norm import normalize_country_names

import os


load_dotenv()

spark = (
    SparkSession.builder
    .appName("ExternalDataProcessing")
    .config(
        "spark.jars.packages",
        "net.snowflake:spark-snowflake_2.13:3.2.1-spark_4.1,"
        "net.snowflake:snowflake-jdbc:4.0.2"
    )
    .getOrCreate()
)

data_dir = Path("data/raw")

population = spark.read.csv(
    str(data_dir / "merged_2020_2025_by_country_final.csv"),
    header=True,
    inferSchema=True
)

gdp = spark.read.csv(
    str(data_dir / "gdp-per-capita-worldbank.csv"),
    header=True,
    inferSchema=True
)

density = spark.read.csv(
    str(data_dir / "population-density.csv"),
    header=True,
    inferSchema=True
)

# population.printSchema()
# gdp.printSchema()
# density.printSchema()

# because years are stored as separate columns, I convert it from wide format to long format
# and restrict possible years to the range of 2020-2023
population_long = population.select(
    F.col("country_clean").alias("Country"),
    F.expr("""
        stack(
            4,
            2020, `2020`,
            2021, `2021`,
            2022, `2022`,
            2023, `2023`
        ) as (Year, Population)
    """)
)

# population_long.printSchema()
# print(population_long.show())

# Rename column entity to country and as was done previously with population - 
# restrict possible years to the range of 2020-2023
gdp_clean = (
    gdp
    .select(
        F.col("Entity").alias("Country"),
        F.col("Year"),
        F.col("GDP per capita").alias("GDP_per_capita")
    )
    .filter(
        F.col("Year").between(2020, 2023)
    )
)

# print(gdp_clean.show())

# The same logic is applied as for gdp dataset
density_clean = (
    density
    .select(
        F.col("Entity").alias("Country"),
        F.col("Year"),
        F.col("Population density").alias("Population_density")
    )
    .filter(
        F.col("Year").between(2020, 2023)
    )
)

# print(density_clean.show())



# normalize all country names
population_long = normalize_country_names(population_long)
gdp_clean = normalize_country_names(gdp_clean)
density_clean = normalize_country_names(density_clean)

# mergin all three datasets into one
combined = (
    population_long
    .join(
        gdp_clean,
        on=["Country", "Year"],
        how="left"
    )
    .join(
        density_clean,
        on=["Country", "Year"],
        how="left"
    )
)

combined.show(20, truncate=False)
combined.printSchema()

# there likely to be null values because datasets may have difference country names
combined.select(
    F.sum(
        F.when(F.col("Population").isNull(), 1).otherwise(0)
    ).alias("missing_population"),

    F.sum(
        F.when(F.col("GDP_per_capita").isNull(), 1).otherwise(0)
    ).alias("missing_gdp"),

    F.sum(
        F.when(F.col("Population_density").isNull(), 1).otherwise(0)
    ).alias("missing_density")
).show()


combined.filter(
    F.col("GDP_per_capita").isNull()
).select("Country").distinct().show(100, truncate=False)

combined.filter(
    F.col("Population_density").isNull()
).select("Country").distinct().show(100, truncate=False)

gdp_clean.filter(
    F.col("Country").isin(
        "Yemen",
        "Korea, North",
        "Eritrea",
        "Western Sahara",
        "Venezuela, Bolivarian Republic of",
        "Cuba",
        "Monaco",
        "French Polynesia",
        "Syria",
        "French Guiana",
        "Taiwan, Province of China",
        "South Sudan"
    )
).orderBy("Country", "Year").show(100, truncate=False)


# save the data locally
combined.coalesce(1).write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/processed/country_demographics_2020_2023")


sfOptions = {
    "sfURL": os.getenv("SNOWFLAKE_URL"),
    "sfUser": os.getenv("SNOWFLAKE_USER"),
    "sfPassword": os.getenv("SNOWFLAKE_PASSWORD"),
    "sfDatabase": "COVID_ANALYTICS",
    "sfSchema": "EXTERNAL_DATA",
    "sfWarehouse": "COMPUTE_WH"
}

combined.write \
    .format("snowflake") \
    .options(**sfOptions) \
    .option("dbtable", "COUNTRY_DEMOGRAPHICS") \
    .mode("overwrite") \
    .save()