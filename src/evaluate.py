from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score
from math import sqrt

def evaluate_model(model, X_val, y_val):
    """
    Evaluates the trained model using RMSE, MAPE, and R².

    Args:
        model: The trained model.
        X_val (pandas.DataFrame): The validation features.
        y_val (pandas.Series): The actual validation labels.

    Returns:
        tuple: RMSE, MAPE, R²
    """
    y_val_pred = model.predict(X_val)
    rmse = sqrt(mean_squared_error(y_val, y_val_pred))
    mape = mean_absolute_percentage_error(y_val, y_val_pred) * 100  # Convert to percentage
    r2 = r2_score(y_val, y_val_pred)
    return rmse, mape, r2