import time
from tqdm import tqdm
from src.preprocessing import apply_filters

def process_images(images):
    """
    Processes images sequentially.

    Parameters:
        - images (list): List of images to process.
    Returns:
        - processed_images (list): List of dictionaries containing filtered images.
    """
    processed_images = []
    for image in tqdm(images):  # Process all images
        filtered_images = apply_filters(image)
        processed_images.append(filtered_images)
    return processed_images

def sequential_execution(yes_images, no_images):
    """
    Executes the sequential version of the pipeline.

    Parameters:
        - yes_images (list): List of images with tumors.
        - no_images (list): List of images without tumors.
    Returns:
        - execution_time (float): Time taken for execution.
    """
    start_time = time.time()
    yes_inputs = process_images(yes_images)
    no_inputs = process_images(no_images)
    end_time = time.time()
    
    execution_time = end_time - start_time
    return execution_time