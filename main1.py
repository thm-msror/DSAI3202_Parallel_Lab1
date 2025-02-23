from src.data_loader import load_data
from src.preprocessing import split_data
from src.serial_bestParameters import serial_search
from src.thread_bestParameters import thread_search
from src.process_bestParameters import process_search
from src.performance import compute_speedup, compute_efficiency, amdahls_law, gustafsons_law

# Load and preprocess data
train_data_cleaned = load_data()
X_train, X_val, y_train, y_val = split_data(train_data_cleaned)

# Run searches
serial_time, serial_rmse, serial_mape, serial_r2, serial_params = serial_search(X_train, X_val, y_train, y_val)
thread_time, thread_rmse, thread_mape, thread_r2, thread_params = thread_search(X_train, X_val, y_train, y_val)
process_time, process_rmse, process_mape, process_r2, process_params = process_search(X_train, X_val, y_train, y_val)

# Print results
print(f"Serial Search: Time = {serial_time:.2f}s, RMSE = {serial_rmse:.4f}, MAPE = {serial_mape:.4f}%, R² = {serial_r2:.4f}, Params = {serial_params}")
print(f"Thread Search: Time = {thread_time:.2f}s, RMSE = {thread_rmse:.4f}, MAPE = {thread_mape:.4f}%, R² = {thread_r2:.4f}, Params = {thread_params}")
print(f"Process Search: Time = {process_time:.2f}s, RMSE = {process_rmse:.4f}, MAPE = {process_mape:.4f}%, R² = {process_r2:.4f}, Params = {process_params}")

# Calculate speedups
thread_speedup = compute_speedup(serial_time, thread_time)
process_speedup = compute_speedup(serial_time, process_time)

# Number of parallel units (e.g., number of threads or processes)
num_threads = 6
num_processes = 6

# Compute efficiency for threading and multiprocessing
thread_efficiency = compute_efficiency(thread_speedup, num_threads)
process_efficiency = compute_efficiency(process_speedup, num_processes)

# Example of parallel fraction (P)
parallel_fraction = 0.21  

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