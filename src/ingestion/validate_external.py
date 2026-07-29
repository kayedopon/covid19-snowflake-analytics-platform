import pyspark.sql.functions as F


def validate_external_data(combined):
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