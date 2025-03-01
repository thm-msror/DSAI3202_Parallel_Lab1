import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from src.preprocessing import apply_filters
from tqdm import tqdm
import math

def process_chunk(chunk):
    """Process a chunk of images using list comprehension"""
    return [apply_filters(img) for img in chunk]

def parallel_execution(yes_images, no_images, max_workers=None, chunk_size=None):
    """
    Optimized parallel execution with dynamic chunk sizing and reduced overhead
    """
    start_time = time.time()
    max_workers = max_workers or cpu_count()
    
    # Combine datasets for balanced processing
    all_images = yes_images + no_images
    labels = [1] * len(yes_images) + [0] * len(no_images)
    
    # Dynamic chunk sizing based on worker count and dataset size
    total_images = len(all_images)
    chunk_size = chunk_size or max(1, math.ceil(total_images / (max_workers * 2)))
    chunks = [all_images[i:i + chunk_size] for i in range(0, total_images, chunk_size)]
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks first
        futures = {executor.submit(process_chunk, chunk): i for i, chunk in enumerate(chunks)}
        
        # Collect results with progress bar
        results = []
        with tqdm(total=len(chunks), desc="Processing") as pbar:
            for future in as_completed(futures):
                chunk_idx = futures[future]
                results.extend(future.result())
                pbar.update(1)
    
    # Separate results back into yes/no
    yes_results = [r for r, l in zip(results, labels) if l == 1]
    no_results = [r for r, l in zip(results, labels) if l == 0]
    
    return time.time() - start_time, yes_results, no_results