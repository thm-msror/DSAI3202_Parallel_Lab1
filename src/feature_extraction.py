import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import skimage.feature as feature
from skimage.feature import hog, local_binary_pattern
from multiprocessing import cpu_count
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler

def compute_glcm_features(args):
    """Compute GLCM features."""
    image, filter_name = args
    image = (image * 255).astype(np.uint8)
    graycom = feature.graycomatrix(
        image, 
        distances=[1, 3, 5],  # Added more distances
        angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
        levels=256,
        symmetric=True
    )
    features = {}
    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation']:
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

def compute_lbp_features(image):
    """Compute Local Binary Patterns (LBP) features."""
    lbp = local_binary_pattern(image, P=8, R=1, method="uniform")
    hist, _ = np.histogram(lbp, bins=np.arange(0, 10), range=(0, 9))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-6)  # Normalize histogram
    return hist

def process_single_image(args):
    """Process a single image with GLCM, HOG, and LBP features."""
    filtered_images, tumor_presence = args
    features = {}
    for key, img in filtered_images.items():
        features.update(compute_glcm_features((img, key)))
        features.update({f'{key}_hog': compute_hog_features(img)})
        features.update({f'{key}_lbp': compute_lbp_features(img)})
    features['Tumor'] = tumor_presence
    return features

def process_batch(batch):
    """Process a batch of images"""
    return [process_single_image((img, label)) for img, label in batch]
    

def create_dataframe(yes_inputs, no_inputs):
    """Create DataFrame with enhanced features."""
    with ProcessPoolExecutor(cpu_count()) as executor:
        # Process in batches of 20 images
        batch_size = 20
        yes_batches = [yes_inputs[i:i + batch_size] for i in range(0, len(yes_inputs), batch_size)]
        no_batches = [no_inputs[i:i + batch_size] for i in range(0, len(no_inputs), batch_size)]
        
        futures = []
        for batch in yes_batches:
            futures.append(executor.submit(process_batch, [(img, 1) for img in batch]))
        for batch in no_batches:
            futures.append(executor.submit(process_batch, [(img, 0) for img in batch]))
        
        results = []
        for future in tqdm(as_completed(futures), total=len(futures), desc="Feature Extraction"):
            results.extend(future.result())
    
    # Convert to DataFrame and normalize features
    dataframe = pd.DataFrame(results)
    scaler = StandardScaler()
    X = dataframe.drop(columns=['Tumor'])
    X_scaled = scaler.fit_transform(X)
    dataframe[X.columns] = X_scaled
    
    return dataframe.sample(frac=1)