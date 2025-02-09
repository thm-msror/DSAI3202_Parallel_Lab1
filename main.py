from src.serialVersion import serial_main
from src.threadVersion import thread_main
from src.processVersion import process_main
from src.performance import compute_speedup, compute_efficiency, amdahls_law, gustafsons_law

serial_time = serial_main()
thread_time = thread_main()
process_time = process_main()

# Compute speedup for threading and multiprocessing
thread_speedup = compute_speedup(serial_time, thread_time)
process_speedup = compute_speedup(serial_time, process_time)

# Number of parallel units (e.g., number of threads or processes)
num_threads = 6
num_processes = 6

# Compute efficiency for threading and multiprocessing
thread_efficiency = compute_efficiency(thread_speedup, num_threads)
process_efficiency = compute_efficiency(process_speedup, num_processes)

# Print results
print(f"\nThreading Speedup: {thread_speedup}")
print(f"Multiprocessing Speedup: {process_speedup}")

print(f"\nThreading Efficiency: {thread_efficiency}")
print(f"Multiprocessing Efficiency: {process_efficiency}")