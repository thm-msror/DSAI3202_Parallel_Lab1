import multiprocessing
import time
from src.generate_random import join_random_letters, add_random_numbers
# Measure the total time for both operations
def process_main(num = 1000000):
    total_start_time = time.time()
    #Seperating the data into 3 different chunks for each function to operate on different data
    start1 = 0
    end1 = num//3
    start2 = num//3
    end2 = 2*num//3
    start3 = 2*num//3
    end3 = num
    # Create processes for letters
    process_letters1 = multiprocessing.Process(target=join_random_letters, args=(start1, end1))
    process_letters2 = multiprocessing.Process(target=join_random_letters, args=(start2, end2))
    process_letters3 = multiprocessing.Process(target=join_random_letters, args=(start3, end3))
    # Create processes for numbers
    process_numbers1 = multiprocessing.Process(target=add_random_numbers, args=(start1, end1))
    process_numbers2 = multiprocessing.Process(target=add_random_numbers, args=(start2, end2))
    process_numbers3 = multiprocessing.Process(target=add_random_numbers, args=(start3, end3))
    # Start the processes
    process_letters1.start()
    process_letters2.start()
    process_letters3.start()
    process_numbers1.start()
    process_numbers2.start()
    process_numbers3.start()
    # Wait for all processes to finish
    process_letters1.join()
    process_letters2.join()
    process_letters3.join()
    process_numbers1.join()
    process_numbers2.join()
    process_numbers3.join()
    total_end_time = time.time()
    print(f"Total time taken for the process version: {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time