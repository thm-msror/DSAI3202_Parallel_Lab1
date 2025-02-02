import time
from src.generate_random import join_random_letters, add_random_numbers

# Measure the total time for both operations
def serial_main(end_letters= 1000000):
    total_start_time = time.time()
    
    join_random_letters(end = end_letters)
    add_random_numbers(end = end_letters)
    
    total_end_time = time.time()
    print(f"Total time taken for the serial version: {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time
