import time
from math import sqrt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from src.preprocessing import split_data  # Only needed if split_data() hasn't been executed before
from src.data_loader import load_data  # Only needed if load_data() hasn't been executed before
from src.evaluate import evaluate_model  # Import if evaluation functions are used elsewhere
from src.model import train_model  # Importing in case we need the trained model

def serial_search(X_train_filled, X_val_filled, y_train, y_val):
    start_time = time.time()

    # Define the parameter ranges
    n_estimators_range = [10, 25, 50, 100, 200, 300, 400]
    max_features_range = ['sqrt', 'log2', None]  # None means using all features
    max_depth_range = [1, 2, 5, 10, 20, None]  # None means no limit

    # Initialize variables to store the best model and its RMSE and parameters
    best_rmse = float('inf')
    best_mape = float('inf')
    best_model = None
    best_parameters = {}

    # Loop over all possible combinations of parameters
    for n_estimators in n_estimators_range:
        for max_features in max_features_range:
            for max_depth in max_depth_range:
                # Create and train the Random Forest model
                rf_model = RandomForestRegressor(
                    n_estimators=n_estimators,
                    max_features=max_features,
                    max_depth=max_depth,
                    random_state=42
                )
                rf_model.fit(X_train_filled, y_train)
                
                # Make predictions and compute RMSE
                y_val_pred = rf_model.predict(X_val_filled)
                rmse = sqrt(mean_squared_error(y_val, y_val_pred))
                mape = mean_absolute_percentage_error(y_val, y_val_pred) * 100

                # Update best model if current model is better
                if rmse < best_rmse:
                    best_rmse = rmse
                    best_mape = mape
                    best_model = rf_model
                    best_parameters = {
                        'n_estimators': n_estimators,
                        'max_features': max_features,
                        'max_depth': max_depth
                    }

    end_time = time.time()
    sequential_time = end_time - start_time

    print(f"Sequential Execution Time: {sequential_time} seconds")

    return sequential_time
