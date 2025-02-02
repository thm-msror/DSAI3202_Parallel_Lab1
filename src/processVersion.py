import multiprocessing
import time
from src.generate_random import join_random_letters, add_random_numbers

# Measure the total time for both operations
def process_main():
    total_start_time = time.time()

    # Create processes for letters and numbers
    process_letters1 = multiprocessing.Process(target=join_random_letters)
    process_letters2 = multiprocessing.Process(target=join_random_letters)
    
    process_numbers1 = multiprocessing.Process(target=add_random_numbers)
    process_numbers2 = multiprocessing.Process(target=add_random_numbers)

    # Start the processes
    process_letters1.start()
    process_letters2.start()
    
    process_numbers1.start()
    process_numbers2.start()

    # Wait for all processes to finish
    process_letters1.join()
    process_letters2.join()
    
    process_numbers1.join()
    process_numbers2.join()

    total_end_time = time.time()
    print(f"Total time taken for the process version: {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time