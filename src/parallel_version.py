import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager, cpu_count
from tqdm import tqdm
from src.preprocessing import apply_filters

def process_image(image):
    """
    Processes a single image (must be top-level for multiprocessing).

    Parameters:
        - image: Input image.
    Returns:
        - filtered_images (dict): Dictionary of filtered images.
    """
    return apply_filters(image)

def process_chunk(images):
    """
    Processes a chunk of images.

    Parameters:
        - images (list): List of images to process.
    Returns:
        - results (list): List of processed images.
    """
    return [process_image(img) for img in images]

def parallel_execution(yes_images, no_images, max_workers=None, chunk_size=10):
    """
    Executes the parallel version of the pipeline using ProcessPoolExecutor.

    Parameters:
        - yes_images (list): List of images with tumors.
        - no_images (list): List of images without tumors.
        - max_workers (int): Number of parallel workers (default: cpu_count()).
        - chunk_size (int): Number of images per chunk.

    Returns:
        - execution_time (float): Time taken for execution.
        - yes_results (list): Processed 'yes' images.
        - no_results (list): Processed 'no' images.
    """
    start_time = time.time()
    max_workers = max_workers or cpu_count()  # Use all available cores

    # Use Manager for shared resources
    manager = Manager()
    yes_results = manager.list()  # Shared list for 'yes' results
    no_results = manager.list()   # Shared list for 'no' results

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks for 'yes' images in chunks
        yes_chunks = [yes_images[i:i + chunk_size] for i in range(0, len(yes_images), chunk_size)]
        yes_futures = [executor.submit(process_chunk, chunk) for chunk in yes_chunks]
        
        # Submit tasks for 'no' images in chunks
        no_chunks = [no_images[i:i + chunk_size] for i in range(0, len(no_images), chunk_size)]
        no_futures = [executor.submit(process_chunk, chunk) for chunk in no_chunks]

        # Use tqdm for progress tracking
        for future in tqdm(as_completed(yes_futures + no_futures), total=len(yes_futures) + len(no_futures), desc="Parallel Processing"):
            result = future.result()
            if future in yes_futures:
                yes_results.extend(result)  # Safely extend shared list with the results
            else:
                no_results.extend(result)  # Safely extend shared list with the results

    execution_time = time.time() - start_time
    return execution_time, list(yes_results), list(no_results)