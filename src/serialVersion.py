import time
from src.sum_num import compute_sum
# Measure the total time for both operations
def serial_main(n= 100_000_000):
    total_start_time = time.time()
    seq_sum = compute_sum(1, n)
    total_end_time = time.time()
    print(f"Execution time with serial: {total_end_time - total_start_time} seconds")
    print(f"Sequential Sum: {seq_sum}")
    return total_end_time - total_start_time