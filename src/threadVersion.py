import threading
import queue
import time
from src.sum_num import compute_sum
def thread_main(n=100_000_000, num_threads=10):
    """Divide the range into chunks, assign each to a thread, and compute the sum in parallel."""
    total_start_time = time.time()
    chunk_size = n // num_threads
    threads = []
    result_queue = queue.Queue()  # Using queue instead of list for thread-safe results
    # Worker function inside thread_main
    def thread_worker(start, end):
        result_queue.put(compute_sum(start, end))  # Put the result into the queue
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        if i == num_threads - 1:
            end = n  # Ensure last thread covers remaining numbers
        thread = threading.Thread(target=thread_worker, args=(start, end))
        threads.append(thread)
        thread.start()
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    # Collect all results from the queue
    total_sum = 0
    while not result_queue.empty():
        total_sum += result_queue.get()
    total_end_time = time.time()
    print(f"Execution time with threading: {total_end_time - total_start_time} seconds")
    print(f"Threaded Sum: {total_sum}")
    return total_end_time - total_start_time