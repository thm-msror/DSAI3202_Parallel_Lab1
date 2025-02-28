import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from src.preprocessing import apply_filters
from tqdm import tqdm
import math

def process_chunk(chunk):
    return [apply_filters(img) for img in chunk]

def parallel_execution(yes_images, no_images, max_workers=None, chunk_size=10):
    """
    Optimized version with better chunking and reduced overhead
    """
    start_time = time.time()
    max_workers = max_workers or cpu_count()
    
    # Combine datasets for balanced processing
    all_images = yes_images + no_images
    labels = [1]*len(yes_images) + [0]*len(no_images)
    
    # Dynamic chunk sizing based on worker count
    chunk_size = max(1, math.ceil(len(all_images) / (max_workers * 2)))
    chunks = [all_images[i:i+chunk_size] for i in range(0, len(all_images), chunk_size)]
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_chunk, chunk): i for i, chunk in enumerate(chunks)}
        
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