import time
import multiprocessing
from src.sum_num import compute_sum
def process_main(n=100_000_000, num_processes=6):
    """Divide the range into chunks, assign each to a process, and compute the sum in parallel."""
    total_start_time = time.time()
    chunk_size = n // num_processes
    processes = []
    result_queue = multiprocessing.Queue()  # Creates a multiprocessing queue for inter-process communication.
    # Worker function inside process_main
    def process_worker(start, end, queue):
        partial_sum = compute_sum(start, end)
        queue.put(partial_sum) # adding the partial sums in the queue
    # Create and start processes
    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        if i == num_processes - 1:
            end = n  # Ensure last process covers remaining numbers
        process = multiprocessing.Process(target=process_worker, args=(start, end, result_queue))
        processes.append(process)
        process.start()
    # Wait for all processes to finish
    for process in processes:
      process.join()
    # Compute total sum manually
    total_sum = 0
    for _ in range(num_processes):
        partial_sum = result_queue.get()
        total_sum += partial_sum
    total_end_time = time.time()
    print(f"Execution time with multiprocessing: {total_end_time - total_start_time} seconds")
    print(f"Multiprocessing Sum: {total_sum}")  
    return total_end_time - total_start_time