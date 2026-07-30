import numpy as np
from prophet import Prophet


def train_prophet_model(train_df):
    prophet_df = train_df[["date", "cases_7d_avg"]].copy()

    prophet_df = prophet_df.rename(
        columns={
            "date": "ds",
            "cases_7d_avg": "y"
        }
    )

    # Log-transform the target.
    # This helps prevent unrealistic negative forecasts.
    prophet_df["y"] = np.log1p(prophet_df["y"])

    model = Prophet(
        growth="linear",
        daily_seasonality=False,
        weekly_seasonality=False,
        yearly_seasonality=True,
        changepoint_prior_scale=0.2
    )

    model.fit(prophet_df)

    return model


def prophet_forecast(model, periods):
    future = model.make_future_dataframe(
        periods=periods,
        freq="D"
    )

    forecast = model.predict(future)

    result = forecast.tail(periods)[
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ].copy()

    result = result.rename(
        columns={
            "ds": "date",
            "yhat": "predicted_cases",
            "yhat_lower": "lower_bound",
            "yhat_upper": "upper_bound"
        }
    )

    # Convert predictions back from log scale.
    result["predicted_cases"] = np.expm1(result["predicted_cases"])
    result["lower_bound"] = np.expm1(result["lower_bound"])
    result["upper_bound"] = np.expm1(result["upper_bound"])

    # Safety only.
    result["predicted_cases"] = result["predicted_cases"].clip(lower=0)
    result["lower_bound"] = result["lower_bound"].clip(lower=0)

    return result.reset_index(drop=True)