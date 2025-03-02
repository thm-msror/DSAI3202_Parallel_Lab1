import time
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from src.preprocessing import apply_filters
from tqdm import tqdm

def process_chunk(chunk):
    """Process a chunk of images by applying filters."""
    return [apply_filters(img) for img in chunk]

def parallel_execution(yes_images, no_images, max_workers=None, chunk_size=10):
    """
    Optimized parallel execution with dynamic chunk sizing and proper error management.
    
    Parameters:
        yes_images (list): List of images with tumors.
        no_images (list): List of images without tumors.
        max_workers (int): Number of parallel workers.
        chunk_size (int): Number of images per chunk.
        
    Returns:
        execution_time (float): Time taken for parallel processing.
        yes_results (list): Processed images with tumor.
        no_results (list): Processed images without tumor.
    """
    start_time = time.time()
    max_workers = max(1, cpu_count() - 1) if max_workers is None else max_workers
    
    # Combine all images and their labels
    all_images = yes_images + no_images
    labels = [1] * len(yes_images) + [0] * len(no_images)
    
    total_images = len(all_images)
    num_chunks = math.ceil(total_images / chunk_size)
    chunks = [all_images[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]
    
    results = [None] * num_chunks
    
    try:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_chunk, chunk): idx for idx, chunk in enumerate(chunks)}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Parallel Processing"):
                idx = futures[future]
                results[idx] = future.result()
    except KeyboardInterrupt:
        print("Parallel processing interrupted by user. Shutting down...")
        executor.shutdown(wait=False)
        raise
    
    # Flatten the results and preserve order
    ordered_results = [img for chunk in results if chunk for img in chunk]
    
    # Separate images based on original labels
    yes_results = [img for img, label in zip(ordered_results, labels) if label == 1]
    no_results = [img for img, label in zip(ordered_results, labels) if label == 0]
    
    exec_time = time.time() - start_time
    return exec_time, yes_results, no_results
