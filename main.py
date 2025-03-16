import random
from src.sequential import sequential_execution
from src.multiprocessing_loop import multiprocessing_execution
from src.multiprocessing_pool import multiprocessing_pool_map, multiprocessing_pool_apply
from src.concurrent_executor import concurrent_execution

def run_tests(size):
    """Runs all execution methods and compares performance."""
    print(f"\nTesting with {size} numbers...")

    numbers = [random.randint(1, 100) for _ in range(size)]
    
    # Sequential execution
    _, time_seq = sequential_execution(numbers)
    print(f"Sequential execution: {time_seq:.4f} seconds")

    # Multiprocessing with individual processes
    _, time_mp_loop = multiprocessing_execution(numbers)
    print(f"Multiprocessing (loop): {time_mp_loop:.4f} seconds")

    # Multiprocessing pool (map & map_async)
    _, time_mp_map, time_mp_map_async = multiprocessing_pool_map(numbers)
    print(f"Multiprocessing pool (map): {time_mp_map:.4f} seconds")
    print(f"Multiprocessing pool (map_async): {time_mp_map_async:.4f} seconds")

    # Multiprocessing pool (apply & apply_async)
    _, time_mp_apply, time_mp_apply_async = multiprocessing_pool_apply(numbers)
    print(f"Multiprocessing pool (apply): {time_mp_apply:.4f} seconds")
    print(f"Multiprocessing pool (apply_async): {time_mp_apply_async:.4f} seconds")

    # Concurrent futures execution
    _, time_concurrent = concurrent_execution(numbers)
    print(f"Concurrent.futures execution: {time_concurrent:.4f} seconds")

if __name__ == "__main__":
    run_tests(10**6)  # Test with 10^6 numbers
    print("\n")
    run_tests(10**7)  # Test with 10^7 numbers