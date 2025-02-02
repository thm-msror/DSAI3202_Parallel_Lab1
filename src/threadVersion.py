import threading
import time
from src.generate_random import join_random_letters, add_random_numbers

# Measure the total time for both operations
def thread_main(num = 1000000):
    total_start_time = time.time()
    
    #Seperating the data into 3 different chunks for each function to operate on different data
    start1 = 0
    end1 = num//3
    start2 = num//3
    end2 = 2*num//3
    start3 = 2*num//3
    end3 = num
    
    # Create threads for letters generation and joining
    thread_letters1 = threading.Thread(target=join_random_letters, args=(start1, end1))
    thread_letters2 = threading.Thread(target=join_random_letters, args= (start2, end2))
    thread_letters3 = threading.Thread(target=join_random_letters, args= (start3, end3))
    
    # Create threads for number generation and addition
    thread_numbers1 = threading.Thread(target=add_random_numbers, args= (start1, end1))
    thread_numbers2 = threading.Thread(target=add_random_numbers, args= (start2, end2))
    thread_numbers3 = threading.Thread(target=add_random_numbers, args= (start3, end3))

    # Start the threads
    thread_letters1.start()
    thread_letters2.start()
    thread_letters3.start()
    
    thread_numbers1.start()
    thread_numbers2.start()
    thread_numbers3.start()

    # Wait for all threads to finish
    thread_letters1.join()
    thread_letters2.join()
    thread_letters3.join()
    
    thread_numbers1.join()
    thread_numbers2.join()
    thread_numbers3.join()
    
    total_end_time = time.time()
    print(f"Total time taken for the thread version: {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time