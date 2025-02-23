import time
from multiprocessing import Pool, Manager
from src.model import train_model
from src.evaluate import evaluate_model

def train_and_evaluate_chunk(params_chunk, X_train, X_val, y_train, y_val, results_queue):
    """
    Trains and evaluates a chunk of models, keeping track of the local best parameters.
    Only the local best result is sent to the results_queue.
    """
    local_best_params = None
    local_best_rmse = float('inf')
    local_best_mape = float('inf')
    local_best_r2 = -float('inf')

    for params in params_chunk:
        n_estimators, max_features, max_depth = params
        model = train_model(X_train, y_train, n_estimators=n_estimators, max_features=max_features, max_depth=max_depth)
        rmse, mape, r2 = evaluate_model(model, X_val, y_val)

        if rmse < local_best_rmse:
            local_best_rmse = rmse
            local_best_mape = mape
            local_best_r2 = r2
            local_best_params = params

    # Send only the local best result to the queue
    results_queue.put((local_best_params, local_best_rmse, local_best_mape, local_best_r2))

# Fixed chunk size improves load balancing, reduces overhead, and ensures fault tolerance by distributing work evenly.
def process_search(X_train, X_val, y_train, y_val, num_processes=6, chunk_size=10):
    """
    Performs hyperparameter tuning using multiprocessing with chunking.

    Args:
        X_train, X_val, y_train, y_val: Training and validation data.
        num_processes (int): Number of processes to use.
        chunk_size (int): Number of parameter combinations to process in each chunk.

    Returns:
        tuple: Execution time, best RMSE, best MAPE, best R², best parameters.
    """
    start_time = time.time()

    # Define hyperparameter ranges
    n_estimators_range = [10, 25, 50, 100, 200, 300, 400]
    max_features_range = ['sqrt', 'log2', None]
    max_depth_range = [1, 2, 5, 10, 20, None]

    # Generate all combinations of parameters
    param_combinations = [
        (n_estimators, max_features, max_depth)
        for n_estimators in n_estimators_range
        for max_features in max_features_range
        for max_depth in max_depth_range
    ]

    # Use a Manager to create a process-safe queue
    manager = Manager()
    results_queue = manager.Queue()

    # Split parameter combinations into chunks
    param_chunks = [param_combinations[i:i + chunk_size] for i in range(0, len(param_combinations), chunk_size)]

    # Create a pool of workers
    with Pool(processes=num_processes) as pool:
        # Distribute the work among the processes
        pool.starmap(
            train_and_evaluate_chunk,
            [(chunk, X_train, X_val, y_train, y_val, results_queue) for chunk in param_chunks]
        )

    # Collect results from the queue
    results = []
    while not results_queue.empty():
        results.append(results_queue.get())

    # Find the overall best parameters (lowest RMSE)
    best_params = None
    best_rmse = float('inf')
    best_mape = float('inf')
    best_r2 = -float('inf')
    for params, rmse, mape, r2 in results:
        if rmse < best_rmse:
            best_rmse = rmse
            best_mape = mape
            best_r2 = r2
            best_params = params

    end_time = time.time()
    execution_time = end_time - start_time

    return execution_time, best_rmse, best_mape, best_r2, best_params