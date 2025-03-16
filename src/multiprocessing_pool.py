import time
import multiprocessing
from src.compute_square import square

def multiprocessing_pool_map(numbers):
    """Executes using multiprocessing pool with map()."""
    start_time = time.time()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(square, numbers)
    end_time = time.time()
    
    start_time1 = time.time()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map_async(square, numbers)
    end_time1 = time.time()
    
    return results, end_time - start_time, end_time1 - start_time1

def multiprocessing_pool_apply(numbers):
    """Executes using multiprocessing pool with apply()."""
    start_time = time.time()
    results = []
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for num in numbers:
            results.append(pool.apply(square, args=(num,)))
    end_time = time.time()
    
    start_time1 = time.time()
    results = []
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for num in numbers:
            results.append(pool.apply_async(square, args=(num,)))
    end_time1 = time.time()
    
    return results, end_time - start_time, end_time1 - start_time1