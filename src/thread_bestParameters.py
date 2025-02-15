import time
import threading
from queue import Queue
from src.model import train_model
from src.evaluate import evaluate_model

def thread_search(X_train, X_val, y_train, y_val, num_threads=6):
    # Record the start time
    start_time = time.time()

    # Define the hyperparameter ranges to search
    n_estimators_range = [10, 25, 50, 100, 200, 300, 400]
    max_features_range = ['sqrt', 'log2', None]
    max_depth_range = [1, 2, 5, 10, 20, None]

    # Generate all combinations of parameters
    param_combinations = []
    for n_estimators in n_estimators_range:
        for max_features in max_features_range:
            for max_depth in max_depth_range:
                param_combinations.append((n_estimators, max_features, max_depth))

    # Calculate chunk size
    n = len(param_combinations)
    chunk_size = n // num_threads

    # Initialize lists to store threads and a queue for results
    threads = []
    results_queue = Queue()

    def thread_worker(start, end, results_queue):
        # Process a chunk of parameter combinations
        for i in range(start, end):
            params = param_combinations[i]
            n_estimators, max_features, max_depth = params  # Unpacking the tuple params, (10, 'sqrt', 1) where n_estimators=10, max_features='sqrt', max_depth=1
            # Train the model with the given hyperparameters
            model = train_model(X_train, y_train, n_estimators=n_estimators, max_features=max_features, max_depth=max_depth)
            # Evaluate the model and get the RMSE
            rmse = evaluate_model(model, X_val, y_val)
            # Put the results (parameters and RMSE) into the queue
            results_queue.put((params, rmse))
    
    # Create and start threads for each chunk
    for i in range(num_threads):
        start = i * chunk_size
        if i < num_threads - 1:
            end = (i + 1) * chunk_size
        else:
            end = n
        thread = threading.Thread(target=thread_worker, args=(start, end, results_queue))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Record the end time
    end_time = time.time()
    threading_time = end_time - start_time

    # Collect results from the queue
    results = []
    while not results_queue.empty():
        results.append(results_queue.get())

    # Find the best parameters (lowest RMSE)
    best_params = None
    best_rmse = float('inf')
    for params, rmse in results:
        if rmse < best_rmse:
            best_rmse = rmse
            best_params = params

    # Return the execution time, best RMSE, and best parameters
    return threading_time, best_rmse, {'n_estimators': best_params[0], 'max_features': best_params[1], 'max_depth': best_params[2]}