import numpy as np
import pandas as pd
from skimage.feature import graycomatrix, graycoprops, hog
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler

def compute_features(args):
    """
    Computes GLCM and HOG features for a filtered image.
    
    Parameters:
        args (tuple): (filtered_images, label)
    Returns:
        features (dict): Dictionary of computed features with target label.
    """
    try:
        filtered_images, label = args
        features = {}
        for filter_name, img in filtered_images.items():
            # Compute GLCM for one angle (0) to speed things up.
            img_uint8 = (img * 255).astype(np.uint8)
            glcm = graycomatrix(img_uint8, [1], [0], 256, symmetric=True, normed=True)
            features[f'{filter_name}_contrast'] = graycoprops(glcm, 'contrast')[0, 0]
            features[f'{filter_name}_energy'] = graycoprops(glcm, 'energy')[0, 0]
            # Compute HOG features
            hog_feat = hog(img, pixels_per_cell=(32, 32), cells_per_block=(2, 2))
            features[f'{filter_name}_hog_mean'] = hog_feat.mean()
            features[f'{filter_name}_hog_std'] = hog_feat.std()
        features['Tumor'] = label
        return features
    except Exception as e:
        print(f"Error computing features: {e}")
        return None

def create_dataframe(yes_inputs, no_inputs):
    """
    Extracts features from processed images in parallel and returns a normalized, shuffled DataFrame.
    
    Parameters:
        yes_inputs (list): Processed images with tumors.
        no_inputs (list): Processed images without tumors.
    Returns:
        df_normalized (DataFrame): DataFrame with normalized features and target label.
    """
    with ProcessPoolExecutor() as executor:
        futures = []
        for img in yes_inputs:
            futures.append(executor.submit(compute_features, (img, 1)))
        for img in no_inputs:
            futures.append(executor.submit(compute_features, (img, 0)))
        
        results = []
        for future in tqdm(as_completed(futures), total=len(futures), desc="Feature Extraction"):
            res = future.result()
            if res is not None:
                results.append(res)
    
    df = pd.DataFrame(results).dropna()
    if df.empty:
        raise ValueError("No valid features extracted - check input data")
    
    # Data cleaning and normalization
    scaler = StandardScaler()
    X = scaler.fit_transform(df.drop('Tumor', axis=1))
    df_normalized = pd.DataFrame(X, columns=df.columns[:-1])
    df_normalized['Tumor'] = df['Tumor'].values
    
    return df_normalized.sample(frac=1).reset_index(drop=True)
