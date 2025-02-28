import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import skimage.feature as feature
from skimage.feature import hog
from multiprocessing import cpu_count
from tqdm import tqdm  # Corrected import

def compute_glcm_features(args):
    """Compute GLCM features."""
    image, filter_name = args
    image = (image * 255).astype(np.uint8)
    graycom = feature.graycomatrix(
        image, 
        distances=[1, 3], 
        angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
        levels=256,
        symmetric=True
    )
    features = {}
    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy']:
        values = feature.graycoprops(graycom, prop).flatten()
        features.update({f'{filter_name}_{prop}_{i}': v for i, v in enumerate(values)})
    return features

def compute_hog_features(image):
    """Compute HOG features."""
    features, _ = hog(
        image,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        visualize=True,
        multichannel=False
    )
    return features

def process_single_image(args):
    """Process a single image with GLCM and HOG features."""
    filtered_images, tumor_presence = args
    features = {}
    for key, img in filtered_images.items():
        features.update(compute_glcm_features((img, key)))
        features.update({f'{key}_hog': compute_hog_features(img)})
    features['Tumor'] = tumor_presence
    return features

def create_dataframe(yes_inputs, no_inputs):
    """Optimized feature extraction with batched processing"""
    def process_batch(batch):
        return [process_single_image((img, label)) for img, label in batch]

    with ProcessPoolExecutor(cpu_count()) as executor:
        # Process in batches of 20 images
        batch_size = 20
        yes_batches = [yes_inputs[i:i+batch_size] for i in range(0, len(yes_inputs), batch_size)]
        no_batches = [no_inputs[i:i+batch_size] for i in range(0, len(no_inputs), batch_size)]
        
        futures = []
        for batch in yes_batches:
            futures.append(executor.submit(process_batch, [(img, 1) for img in batch]))
        for batch in no_batches:
            futures.append(executor.submit(process_batch, [(img, 0) for img in batch]))
        
        results = []
        for future in tqdm(as_completed(futures), total=len(futures), desc="Feature Extraction"):  # Corrected usage
            results.extend(future.result())
    
    return pd.DataFrame(results).sample(frac=1)