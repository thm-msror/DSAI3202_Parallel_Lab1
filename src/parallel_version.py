# parallel_version.py
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from preprocessing import apply_filters
from multiprocessing import cpu_count
from tqdm import tqdm
import math

def process_chunk(chunk):
    """Process a chunk of images using list comprehension"""
    return [apply_filters(img) for img in chunk]

def parallel_execution(yes_images, no_images, max_workers=None, chunk_size=None):
    """
    Optimized parallel execution with dynamic chunk sizing and direct result aggregation
    """
    start_time = time.time()
    max_workers = max_workers or cpu_count()
    
    # Dynamic chunk sizing based on worker count and dataset size
    total_images = len(yes_images) + len(no_images)
    chunk_size = chunk_size or max(1, math.ceil(total_images / (max_workers * 4)))
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks first
        futures = []
        for dataset in [yes_images, no_images]:
            chunks = [dataset[i:i+chunk_size] for i in range(0, len(dataset), chunk_size)]
            futures += [executor.submit(process_chunk, chunk) for chunk in chunks]
        
        # Collect results with progress bar
        yes_results, no_results = [], []
        yes_count = len(yes_images)
        with tqdm(total=len(futures), desc="Processing") as pbar:
            for i, future in enumerate(as_completed(futures)):
                result = future.result()
                if i < len(futures) // 2:
                    yes_results.extend(result)
                else:
                    no_results.extend(result)
                pbar.update(1)
    
    return time.time() - start_time, yes_results, no_results