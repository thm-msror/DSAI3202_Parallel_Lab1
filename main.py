# main.py
import time
from src.data_loader import load_dataset
from src.sequential_version import sequential_execution
from src.parallel_version import parallel_execution
from multiprocessing import cpu_count

def main():
    # Load dataset
    dataset_path = 'data/brain_tumor_dataset/'
    yes_images, no_images = load_dataset(dataset_path)
    
    # Sequential execution (for testing)
    print("Running sequential version for 5 images...")
    seq_time = sequential_execution(yes_images[:5], no_images[:5])
    print(f"Sequential execution time: {seq_time:.2f} seconds")
    
    # Parallel execution (for testing)
    print("Running parallel version for 5 images...")
    par_time, yes_results, no_results = parallel_execution(yes_images[:5], no_images[:5], max_workers=cpu_count(), chunk_size=2)
    print(f"Parallel execution time: {par_time:.2f} seconds")
    
    # Calculate speedup and efficiency
    speedup = seq_time / par_time
    efficiency = speedup / cpu_count()
    print(f"Speedup: {speedup:.2f}")
    print(f"Efficiency: {efficiency:.2f}")

if __name__ == "__main__":
    main()