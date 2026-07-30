import numpy as np
import pandas as pd

from xgboost import XGBRegressor

from src.forecasting.features import FEATURE_COLUMNS


def create_model():
    return XGBRegressor(
        objective="reg:squarederror",
        n_estimators=500,
        learning_rate=0.03,
        max_depth=5,
        min_child_weight=3,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1
    )


def train_model(train_df: pd.DataFrame):

    model = create_model()

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df["cases_7d_avg"]

    model.fit(
        X_train,
        y_train
    )

    return model


def build_future_features(history_values, prediction_date):
    values = list(history_values)

    features = {
        "lag_1": values[-1],
        "lag_2": values[-2],
        "lag_3": values[-3],
        "lag_7": values[-7],
        "lag_14": values[-14],
        "lag_21": values[-21],
        "lag_28": values[-28],

        "rolling_7": np.mean(values[-7:]),
        "rolling_14": np.mean(values[-14:]),
        "rolling_28": np.mean(values[-28:]),

        "day_of_week": prediction_date.dayofweek,
        "month": prediction_date.month,
        "day_of_year": prediction_date.dayofyear
    }

    return pd.DataFrame([features], columns=FEATURE_COLUMNS)


def recursive_forecast(model, history_df, days=30):
    history_values = history_df["cases_7d_avg"].tolist()
    last_date = history_df["date"].max()
    predictions = []

    for step in range(1, days + 1):
        prediction_date = last_date + pd.Timedelta( days=step)

        features = build_future_features(history_values, prediction_date)
        prediction = float(model.predict(features)[0])

        # negative case forecasts are not accepted
        prediction = max(prediction, 0)

        predictions.append({
            "date": prediction_date,
            "predicted_cases": prediction
        })

        # prediction becomes part of history for
        # prediction of the following day
        history_values.append(prediction)

    return pd.DataFrame(predictions)