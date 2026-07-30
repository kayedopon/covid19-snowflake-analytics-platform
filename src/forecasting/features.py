import pandas as pd


FEATURE_COLUMNS = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_7",
    "lag_14",
    "lag_21",
    "lag_28",
    "rolling_7",
    "rolling_14",
    "rolling_28",
    "day_of_week",
    "month",
    "day_of_year"
]


def create_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    target = "cases_7d_avg"

    df["lag_1"] = df[target].shift(1)
    df["lag_2"] = df[target].shift(2)
    df["lag_3"] = df[target].shift(3)
    df["lag_7"] = df[target].shift(7)
    df["lag_14"] = df[target].shift(14)
    df["lag_21"] = df[target].shift(21)
    df["lag_28"] = df[target].shift(28)

    # shift(1) is important because today's actual
    # target must not be included in today's features
    # to prevent data leakage
    df["rolling_7"] = df[target].shift(1).rolling(7).mean()
    df["rolling_14"] = df[target].shift(1).rolling(14).mean()
    df["rolling_28"] = df[target].shift(1).rolling(28).mean()
    # Calendar features
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day_of_year"] = df["date"].dt.dayofyear

    return df.dropna().reset_index(drop=True)