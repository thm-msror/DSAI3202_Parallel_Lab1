import time
import threading
from src.sum_num import threaded_sum
def thread_main(n=1000000, num_threads=6):
    """Divide the range into chunks, assign each to a thread, and compute the sum in parallel."""
    total_start_time = time.time()
    chunk_size = n // num_threads
    threads = []
    results = [0] * num_threads  # List to store partial sums
    # Create and start threads
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        if i == num_threads - 1:  # Ensure last thread covers remaining numbers
            end = n
        thread = threading.Thread(target=threaded_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    # Collect results from list (partial sums)
    total_sum = sum(results)  # Use sum() since results contains partial sums
    total_end_time = time.time()
    print(f"Execution time with threading: {total_end_time - total_start_time} seconds")
    print(f"Threaded Sum: {total_sum}")
    return total_end_time - total_start_time