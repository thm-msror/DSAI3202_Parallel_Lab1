import time
import multiprocessing
from src.sum_num import process_sum
def process_main(n=1000000, num_processes=6):
    """Divide the range into chunks, assign each to a process, and compute the sum in parallel."""
    total_start_time = time.time()
    chunk_size = n // num_processes
    processes = []
    result_queue = multiprocessing.Queue()  # Queue for storing results
    # Create and start processes
    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        if i == num_processes - 1:  # Ensure last process covers remaining numbers
            end = n
        process = multiprocessing.Process(target=process_sum, args=(start, end, result_queue))
        processes.append(process)
        process.start()
    # Wait for all processes to finish
    for process in processes:
        process.join()
    # Collect results from queue
    total_sum = sum(result_queue.get() for _ in range(num_processes)) 
    total_end_time = time.time()
    print(f"Execution time with multiprocessing: {total_end_time - total_start_time} seconds")
    print(f"Multiprocessing Sum: {total_sum}")
    return total_end_time - total_start_time