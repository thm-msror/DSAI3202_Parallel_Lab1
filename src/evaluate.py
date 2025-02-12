from sklearn.metrics import mean_squared_error
from math import sqrt

def evaluate_model(model, X_val, y_val):
    """
    Evaluates the trained model using RMSE.

    Args:
    model (RandomForestRegressor): The trained model.
    X_val (pandas.DataFrame): The validation features.
    y_val (pandas.Series): The actual validation labels.

    Returns:
    float: RMSE score of the model on the validation data.
    """
    y_val_pred = model.predict(X_val)
    rmse = sqrt(mean_squared_error(y_val, y_val_pred))
    return rmse