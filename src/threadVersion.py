import threading
import time
from src.generate_random import join_random_letters, add_random_numbers

# Measure the total time for both operations
def thread_main(num_letters = 10000, num_numbers = 10000):
    total_start_time = time.time()
    
    start1 = 0
    end1 = num_letters//2
    start2 = num_letters//2
    end2 = num_letters
    
    # Create threads for letters generation and joining
    thread_letters1 = threading.Thread(target=join_random_letters, args =(start1, end1))
    thread_letters2 = threading.Thread(target=join_random_letters, args= (start2, end2))

    # Create threads for number generation and addition
    thread_numbers1 = threading.Thread(target=add_random_numbers, args= (start1, end1))
    thread_numbers2 = threading.Thread(target=add_random_numbers, args= (start2, end2))

    # Start the threads
    thread_letters1.start()
    thread_letters2.start()
    
    thread_numbers1.start()
    thread_numbers2.start()

    # Wait for all threads to finish
    thread_letters1.join()
    thread_letters2.join()
    
    thread_numbers1.join()
    thread_numbers2.join()
    
    total_end_time = time.time()
    print(f"Total time taken for the thread version: {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time