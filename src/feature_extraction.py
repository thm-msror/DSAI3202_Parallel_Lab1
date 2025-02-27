# feature_extraction.py
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import skimage.feature as feature
from multiprocessing import cpu_count

def compute_glcm_features(args):
    """Optimized GLCM computation with reduced memory footprint"""
    image, filter_name = args
    image = (image * 255).astype(np.uint8)
    graycom = feature.graycomatrix(
        image, 
        distances=[1, 3],  # Multiple distances for better features
        angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
        levels=256,
        symmetric=True
    )
    
    features = {}
    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy']:
        values = feature.graycoprops(graycom, prop).flatten()
        features.update({f'{filter_name}_{prop}_{i}': v for i, v in enumerate(values)})
    return features

def process_single_image(args):
    """Wrapper for parallel processing"""
    filtered_images, tumor_presence = args
    features = {}
    for key, img in filtered_images.items():
        features.update(compute_glcm_features((img, key)))
    features['Tumor'] = tumor_presence
    return features

def create_dataframe(yes_inputs, no_inputs):
    """Parallel feature extraction with efficient chunking"""
    def process_dataset(data, label):
        with ProcessPoolExecutor(cpu_count()) as executor:
            args = ((img, label) for img in data)
            return list(executor.map(process_single_image, args, chunksize=10))
    
    yes_features = process_dataset(yes_inputs, 1)
    no_features = process_dataset(no_inputs, 0)
    
    return pd.DataFrame(yes_features + no_features).sample(frac=1)