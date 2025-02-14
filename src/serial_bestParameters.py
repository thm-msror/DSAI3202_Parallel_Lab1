import time
from src.model import train_model
from src.evaluate import evaluate_model
from sklearn.metrics import mean_absolute_percentage_error

def serial_search(X_train, X_val, y_train, y_val):
    # Record the start time of the search process
    start_time = time.time()

    # Define the ranges of hyperparameters to search
    n_estimators_range = [10, 25, 50, 100, 200, 300, 400] # Number of trees in the forest
    max_features_range = ['sqrt', 'log2', None] # Max features to consider for best split
    max_depth_range = [1, 2, 5, 10, 20, None] # Maximum depth of the tree
    
    # Initialize variables to keep track of the best model
    best_rmse = float('inf') # Start with infinity as the best RMSE
    best_mape = float('inf')
    best_params = {} # Dictionary to store the best parameters
    
    # Nested loops to iterate through all combinations of hyperparameters
    for n_estimators in n_estimators_range:
        for max_features in max_features_range:
            for max_depth in max_depth_range:
                # Train a model with the current combination of hyperparameters
                model = train_model(X_train, y_train, n_estimators, max_features, max_depth)
                
                # Evaluate the model and calculate its RMSE
                rmse = evaluate_model(model, X_val, y_val)
                
                # Calculate MAPE
                y_val_pred = model.predict(X_val)
                mape = mean_absolute_percentage_error(y_val, y_val_pred) * 100

                if rmse < best_rmse:
                    best_rmse = rmse
                    best_mape = mape
                    best_params = {'n_estimators': n_estimators, 'max_features': max_features, 'max_depth': max_depth}

    end_time = time.time()
    serial_time = end_time - start_time
    
    # Return the time taken, the best RMSE found, and the corresponding best parameters
    return serial_time, best_rmse, best_params