import numpy as np

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_model(actual, predicted):
    # metrics that are used to assess the fit of model predictions
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    r2 = r2_score(actual, predicted)

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }