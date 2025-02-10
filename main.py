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

# Example of parallel fraction (P) - this will depend on how much work can be parallelized
'''
To calculate the parallel fraction P of a program 
1. count the total number of lines in the program excluding imports, funtion definition (def), function return, comments, empty space lines = 34 - 11 = 23
2. calculate parallel lines of code / total lines of code excluding the exclusions = 5 / 23 = 0.21739 ~= 0.22
'''
parallel_fraction = 0.22 # 22% of the task can be parallelized in the threadVersion.py

# Use Amdahl's and Gustafson's laws for theoretical performance estimation
amdahl_thread = amdahls_law(num_threads, parallel_fraction)
amdahl_process = amdahls_law(num_processes, parallel_fraction)

gustafson_thread = gustafsons_law(num_threads, parallel_fraction)
gustafson_process = gustafsons_law(num_processes, parallel_fraction)

# Print results
print(f"\nThreading Speedup: {thread_speedup}")
print(f"Multiprocessing Speedup: {process_speedup}")

print(f"\nThreading Efficiency: {thread_efficiency}")
print(f"Multiprocessing Efficiency: {process_efficiency}")

print(f"\nAmdahl's Law (Threading): {amdahl_thread}")
print(f"Amdahl's Law (Multiprocessing): {amdahl_process}")

print(f"\nGustafson's Law (Threading): {gustafson_thread}")
print(f"Gustafson's Law (Multiprocessing): {gustafson_process}\n")