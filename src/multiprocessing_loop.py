import time
import multiprocessing
from src.compute_square import square

def worker(n, result_list):
    """Worker function to compute square and store in shared list."""
    result_list.append(square(n))

def multiprocessing_execution(numbers):
    """Executes square function using multiple processes."""
    start_time = time.time()
    processes = []
    manager = multiprocessing.Manager()
    results = manager.list()
    
    for num in numbers:
        p = multiprocessing.Process(target=worker, args=(num, results))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()

    end_time = time.time()
    return list(results), end_time - start_time