import pyspark.sql.functions as F


def normalize_country_names(df):
    # map is used to prevent huge chain of .when()
    mapping_expr = F.create_map(
        *[
            item
            for pair in country_mapping.items()
            for item in (F.lit(pair[0]), F.lit(pair[1]))
        ]
    )

    return df.withColumn(
        "Country",
        F.coalesce(
            mapping_expr[F.col("Country")],
            F.col("Country")
        )
    )


# In order to resolve the issue with country names mismatch 
#I need to do the country-name normalization before joining with Snowflake 
country_mapping = {
    "United States of America": "United States",
    "United States Of America": "United States",
    "USA": "United States",
    "South Korea": "Korea, Republic of",
    "Republic Of Korea": "Korea, Republic of",
    "North Korea": "Korea, North",
    "Democtatic People's Rupublic of Korea": "Korea, North",
    "Democratic Republic of Congo": "Congo, The Democratic Republic of the",
    "Democratic Republic of the Congo": "Congo, The Democratic Republic of the",
    "D R Congo": "Congo, The Democratic Republic of the",
    "Cote d'Ivoire": "Côte d'Ivoire",
    "Ivory Coast": "Côte d'Ivoire",
    "Cape Verde": "Cabo Verde",
    "East Timor": "Timor-Leste",
    "Timor Leste": "Timor-Leste",
    "Brunei": "Brunei Darussalam",
    "Micronesia (country)": "Micronesia",
    "Czech Republic": "Czechia",
    "Swaziland": "Eswatini",
    "Russia": "Russian Federation",
    "Moldova": "Moldova, Republic of",
    "Bolivia": "Bolivia, Plurinational State of",
    "Iran": "Iran, Islamic Republic of",
    "Laos": "Lao People's Democratic Republic",
    "Palestine": "Palestine, State of",
    "Taiwan": "Taiwan, Province of China",
    "Tanzania": "Tanzania, United Republic of",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "Vietnam": "Viet Nam",
    "Guinea Bissau": "Guinea-Bissau",
    "Sao Tome And Principe": "Sao Tome and Principe",
    "Bosnia And Herzegovina": "Bosnia and Herzegovina",
    "Antigua And Barbuda": "Antigua and Barbuda",
    "Trinidad And Tobago": "Trinidad and Tobago",
    "Saint Vincent And The Grenadines":
        "Saint Vincent and the Grenadines",
    "China Hong Kong Sar": "Hong Kong",
    "China Macao Sar": "Macao"
}

