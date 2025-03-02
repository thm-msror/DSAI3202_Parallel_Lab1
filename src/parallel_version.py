import time
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from src.preprocessing import apply_filters
from tqdm import tqdm

def process_chunk(chunk):
    """Process a chunk of images"""
    return [apply_filters(img) for img in chunk]

def parallel_execution(yes_images, no_images, max_workers=None, chunk_size=10):
    """
    Optimized parallel execution with proper chunk handling and error management
    """
    start_time = time.time()
    max_workers = max(1, cpu_count() - 1)  # Leave one core free
    
    # Combine and label datasets
    all_images = yes_images + no_images
    labels = [1] * len(yes_images) + [0] * len(no_images)
    
    # Dynamic chunk sizing
    total_images = len(all_images)
    num_chunks = math.ceil(total_images / chunk_size)
    chunks = [all_images[i * chunk_size:(i + 1) * chunk_size] 
              for i in range(num_chunks)]
    
    # Initialize results list with correct size
    results = [None] * num_chunks
    
    try:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            futures = {executor.submit(process_chunk, chunk): idx 
                      for idx, chunk in enumerate(chunks)}
            
            # Collect results with progress bar
            for future in tqdm(as_completed(futures), total=len(futures), 
                             desc="Parallel Processing"):
                idx = futures[future]
                results[idx] = future.result()
                
    except KeyboardInterrupt:
        print("\nParallel processing interrupted by user. Shutting down...")
        executor.shutdown(wait=False)
        raise
    
    # Flatten results while preserving order
    ordered_results = [img for chunk in results if chunk for img in chunk]
    
    # Separate results using original labels
    yes_results = [img for img, label in zip(ordered_results, labels) if label == 1]
    no_results = [img for img, label in zip(ordered_results, labels) if label == 0]
    
    return time.time() - start_time, yes_results, no_results