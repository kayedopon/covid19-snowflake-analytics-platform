import pyspark.sql.functions as F


def load_external_data(spark, data_dir):
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

    return population, gdp, density


def prepare_population(population):
    """
    This function convert table from wide format to long format 
    because years are stored as separate columns
    Then it restricts possible years to the range of 2020-2023
    """
    return population.select(
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


def prepare_gdp(gdp):
    return (
        gdp
        .select(
            F.col("Entity").alias("Country"),
            F.col("Year"),
            F.col("GDP per capita").alias("GDP_per_capita")
        )
        .filter(F.col("Year").between(2020, 2023))
    )


def prepare_density(density):
    return (
        density
        .select(
            F.col("Entity").alias("Country"),
            F.col("Year"),
            F.col("Population density").alias("Population_density")
        )
        .filter(F.col("Year").between(2020, 2023))
    )


def merge_external_data(population, gdp, density):
    return (
        population
        .join(gdp, on=["Country", "Year"], how="left")
        .join(density, on=["Country", "Year"], how="left")
    )