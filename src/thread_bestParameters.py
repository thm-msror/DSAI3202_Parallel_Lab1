import time
from threading import Thread, Lock
from queue import Queue
from src.model import train_model
from src.evaluate import evaluate_model

def train_and_evaluate_chunk(params_chunk, X_train, X_val, y_train, y_val, results_queue, lock):
    """
    Trains and evaluates a chunk of models with the given parameters.
    Results are stored in the shared results_queue with synchronization.
    """
    for params in params_chunk:
        n_estimators, max_features, max_depth = params
        model = train_model(X_train, y_train, n_estimators=n_estimators, max_features=max_features, max_depth=max_depth)
        rmse, mape, r2 = evaluate_model(model, X_val, y_val)

        # Use a lock to synchronize access to the results queue
        with lock:
            results_queue.put((params, rmse, mape, r2))
            
# Fixed chunk size improves load balancing, reduces overhead, and ensures fault tolerance by distributing work evenly.
def thread_search(X_train, X_val, y_train, y_val, num_threads=6, chunk_size=10):
    """
    Performs hyperparameter tuning using threading with chunking.

    Args:
        X_train, X_val, y_train, y_val: Training and validation data.
        num_threads (int): Number of threads to use.
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

    # Create a thread-safe queue and lock
    results_queue = Queue()
    lock = Lock()

    # Split parameter combinations into chunks
    param_chunks = []
    for i in range(0, len(param_combinations), chunk_size):
        chunk = param_combinations[i:i + chunk_size]
        param_chunks.append(chunk)

    # Function to process tasks from the queue
    def worker():
        while not task_queue.empty():
            chunk = task_queue.get()
            train_and_evaluate_chunk(chunk, X_train, X_val, y_train, y_val, results_queue, lock)
            task_queue.task_done()

    # Create a queue for tasks
    task_queue = Queue()
    for chunk in param_chunks:
        task_queue.put(chunk)

    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Wait for all tasks to be processed
    task_queue.join()

    # Stop the worker threads
    for _ in range(num_threads):
        task_queue.put(None)  # Sentinel value to stop workers
    for thread in threads:
        thread.join()

    # Collect results from the queue
    results = []
    while not results_queue.empty():
        results.append(results_queue.get())

    # Find the best parameters (lowest RMSE)
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