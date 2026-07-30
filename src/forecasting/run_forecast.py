from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.forecasting.data import load_daily_cases, prepare_daily_cases
from src.forecasting.features import create_features, FEATURE_COLUMNS
from src.forecasting.model import train_model, recursive_forecast
from src.forecasting.evaluate import evaluate_model
from src.forecasting.prophet_model import train_prophet_model, prophet_forecast


COUNTRY = "Lithuania"
TEST_DAYS = 14
FORECAST_DAYS = 14

OUTPUT_DIR = Path("outputs/forecasting")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print(f"Loading data for {COUNTRY}")

    raw_df = load_daily_cases(COUNTRY)
    df = prepare_daily_cases(raw_df)

    print("\nPrepared data:")
    print(df.tail())
    print(f"\nNumber of observations: {len(df)}")

    # holdout evaluation
    split_index = len(df) - TEST_DAYS

    historical_train = df.iloc[:split_index].copy()
    test_df = df.iloc[split_index:].copy()

    train_features = create_features(historical_train)

    print("\nTraining period:")
    print(
        historical_train["date"].min(),
        "to",
        historical_train["date"].max()
    )

    print("\nTesting period:")
    print(
        test_df["date"].min(),
        "to",
        test_df["date"].max()
    )

    model = train_model(train_features)

    validation_forecast = recursive_forecast(
        model=model,
        history_df=historical_train,
        days=TEST_DAYS
    )

    actual = test_df["cases_7d_avg"].reset_index(drop=True)
    predicted = validation_forecast["predicted_cases"].reset_index(drop=True)

    baseline_predicted = pd.Series(
        [historical_train["cases_7d_avg"].iloc[-1]] * TEST_DAYS
    )

    metrics = evaluate_model(actual, predicted)
    baseline_metrics = evaluate_model(actual, baseline_predicted)


    recent_prophet_train = historical_train.tail(365)

    prophet_model = train_prophet_model(recent_prophet_train)

    prophet_validation = prophet_forecast(
        prophet_model,
        TEST_DAYS
    )

    prophet_predicted = prophet_validation[
        "predicted_cases"
    ].reset_index(drop=True)

    prophet_metrics = evaluate_model(
        actual,
        prophet_predicted
    )

    print("\nXGBoost validation results")
    print(f"MAE: {metrics['MAE']:.2f}")
    print(f"RMSE: {metrics['RMSE']:.2f}")
    print(f"R²: {metrics['R2']:.4f}")

    print("\nProphet validation results")
    print(f"MAE: {prophet_metrics['MAE']:.2f}")
    print(f"RMSE: {prophet_metrics['RMSE']:.2f}")
    print(f"R²: {prophet_metrics['R2']:.4f}")

    print("\nBaseline validation results")
    print(f"MAE: {baseline_metrics['MAE']:.2f}")
    print(f"RMSE: {baseline_metrics['RMSE']:.2f}")
    print(f"R²: {baseline_metrics['R2']:.4f}")


    #  validation dataframe
    validation_results = pd.DataFrame({
        "date": test_df["date"].reset_index(drop=True),
        "actual": actual,
        "xgboost": predicted,
        "prophet": prophet_predicted,
        "baseline": baseline_predicted
    })

    validation_results.to_csv(
        OUTPUT_DIR / "validation_results.csv",
        index=False
    )


    # validation plot
    plt.figure(figsize=(12, 6))

    plt.plot(
        validation_results["date"],
        validation_results["actual"],
        label="Actual"
    )

    plt.plot(
        validation_results["date"],
        validation_results["xgboost"],
        label="XGBoost"
    )

    plt.plot(
        validation_results["date"],
        validation_results["prophet"],
        label="Prophet"
    )

    plt.plot(
        validation_results["date"],
        validation_results["baseline"],
        label="Baseline"
    )

    plt.xlabel("Date")
    plt.ylabel("7-day average daily cases")
    plt.title(f"{TEST_DAYS}-Day Forecast Validation - {COUNTRY}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "validation_forecast.png", dpi=200)
    plt.close()


    # feature importance
    importance = pd.DataFrame({
        "feature": FEATURE_COLUMNS,
        "importance": model.feature_importances_
    })

    importance = importance.sort_values("importance", ascending=True)

    plt.figure(figsize=(9, 6))
    plt.barh(
        importance["feature"],
        importance["importance"]
    )
    plt.xlabel("Feature Importance")
    plt.title("XGBoost Feature Importance")
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "feature_importance.png", dpi=200)
    plt.close()


    # final model
    all_features = create_features(df)
    final_model = train_model(all_features)

    future_forecast = recursive_forecast(
        model=final_model,
        history_df=df,
        days=FORECAST_DAYS
    )

    future_forecast.to_csv(
        OUTPUT_DIR / "future_forecast.csv",
        index=False
    )

    # Future forecast plot
    historical_plot = df.tail(90)

    plt.figure(figsize=(12, 6))

    plt.plot(
        historical_plot["date"],
        historical_plot["cases_7d_avg"],
        label="Historical"
    )
    plt.plot(
        future_forecast["date"],
        future_forecast["predicted_cases"],
        label="XGBoost Forecast"
    )

    plt.xlabel("Date")
    plt.ylabel("7-day average daily cases")
    plt.title(f"{FORECAST_DAYS}-Day COVID-19 Forecast - {COUNTRY}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "future_forecast.png", dpi=200)
    plt.close()

    print("\nFuture forecast:")
    print(future_forecast)
    print("\nFiles saved to:")
    print(OUTPUT_DIR)

if __name__ == "__main__":
    main()