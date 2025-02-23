import time
from src.model import train_model
from src.evaluate import evaluate_model

def serial_search(X_train, X_val, y_train, y_val):
    """
    Performs hyperparameter tuning using a serial (sequential) approach.

    Args:
        X_train, X_val, y_train, y_val: Training and validation data.

    Returns:
        tuple: Execution time, best RMSE, best MAPE, best R², best parameters.
    """
    start_time = time.time()

    # Define the ranges of hyperparameters to search
    n_estimators_range = [10, 25, 50, 100, 200, 300, 400]
    max_features_range = ['sqrt', 'log2', None]
    max_depth_range = [1, 2, 5, 10, 20, None]

    # Initialize variables to keep track of the best model
    best_rmse = float('inf')
    best_mape = float('inf')
    best_r2 = -float('inf')
    best_params = {}

    # Nested loops to iterate through all combinations of hyperparameters
    for n_estimators in n_estimators_range:
        for max_features in max_features_range:
            for max_depth in max_depth_range:
                # Train and evaluate the model
                model = train_model(X_train, y_train, n_estimators, max_features, max_depth)
                rmse, mape, r2 = evaluate_model(model, X_val, y_val)

                # Update the best parameters if the current model is better
                if rmse < best_rmse:
                    best_rmse = rmse
                    best_mape = mape
                    best_r2 = r2
                    best_params = {'n_estimators': n_estimators, 'max_features': max_features, 'max_depth': max_depth}

    end_time = time.time()
    execution_time = end_time - start_time

    return execution_time, best_rmse, best_mape, best_r2, best_params