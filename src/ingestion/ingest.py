from pathlib import Path

from spark_session import get_session
from transform_external import (
    load_external_data,
    prepare_population,
    prepare_gdp,
    prepare_density,
    merge_external_data
)
from validate_external import validate_external_data
from snowflake_writer import write_to_snowflake

from country_norm import normalize_country_names


spark = get_session()

data_dir = Path("data/raw")

# load data
population, gdp, density = load_external_data(spark, data_dir)

# prepare data
population_long = prepare_population(population)
gdp_clean = prepare_gdp(gdp)
density_clean = prepare_density(density)

# normalize country names
population_long = normalize_country_names(population_long)
gdp_clean = normalize_country_names(gdp_clean)
density_clean = normalize_country_names(density_clean)

combined = merge_external_data(
    population_long,
    gdp_clean,
    density_clean
)

# check how many null values in the final dataset
validate_external_data(combined)

# save dataset localyl
combined.coalesce(1).write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/processed/country_demographics_2020_2023")

write_to_snowflake(combined)