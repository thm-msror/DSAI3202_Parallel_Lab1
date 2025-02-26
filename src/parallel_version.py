# parallel_version.py
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
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

def parallel_execution(yes_images, no_images, max_workers=None):
    """
    Executes the parallel version of the pipeline using ProcessPoolExecutor.

    Parameters:
        - yes_images (list): List of images with tumors.
        - no_images (list): List of images without tumors.
        - max_workers (int): Number of parallel workers (default: cpu_count()).

    Returns:
        - execution_time (float): Time taken for execution.
    """
    start_time = time.time()
    max_workers = max_workers or cpu_count()  # Use all available cores

    # Process only the first 5 images
    yes_images = yes_images[:5]
    no_images = no_images[:5]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks for 'yes' images
        yes_futures = [executor.submit(process_image, img) for img in yes_images]
        
        # Submit tasks for 'no' images
        no_futures = [executor.submit(process_image, img) for img in no_images]

        # Use tqdm for progress tracking
        for future in tqdm(as_completed(yes_futures + no_futures), total=len(yes_futures) + len(no_futures), desc="Parallel Processing"):
            future.result()  # Wait for the result (no need to store for this comparison)

    execution_time = time.time() - start_time
    return execution_time