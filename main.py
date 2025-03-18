import random
import time
from src.sequential import sequential_execution
from src.multiprocessing_pool import multiprocessing_pool_map, multiprocessing_pool_apply
from src.concurrent_executor import concurrent_execution

def run_tests(size):
    """Runs all execution methods and prints performance."""
    print(f"\nTesting with {size} numbers...")

    numbers = [random.randint(1, 100) for _ in range(size)]
    
    print(f"Sequential execution: {sequential_execution(numbers):.4f} seconds")

    time_mp_map, time_mp_map_async = multiprocessing_pool_map(numbers)
    print(f"Multiprocessing pool (map): {time_mp_map:.4f} seconds")
    print(f"Multiprocessing pool (map_async): {time_mp_map_async:.4f} seconds")

    time_mp_apply, time_mp_apply_async = multiprocessing_pool_apply(numbers)
    print(f"Multiprocessing pool (apply): {time_mp_apply:.4f} seconds")
    print(f"Multiprocessing pool (apply_async): {time_mp_apply_async:.4f} seconds")

    print(f"Concurrent.futures execution: {concurrent_execution(numbers):.4f} seconds")

if __name__ == "__main__":
    run_tests(10**6)
    run_tests(10**7)