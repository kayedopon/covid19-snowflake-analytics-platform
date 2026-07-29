from pyspark.sql import SparkSession


def get_session():
    return (
        SparkSession.builder
        .appName("ExternalDataProcessing")
        .config(
            "spark.jars.packages",
            "net.snowflake:spark-snowflake_2.13:3.2.1-spark_4.1,"
            "net.snowflake:snowflake-jdbc:4.0.2"
        )
        .getOrCreate()
    )