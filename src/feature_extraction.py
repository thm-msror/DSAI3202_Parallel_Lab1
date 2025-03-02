import numpy as np
import pandas as pd
from skimage.feature import graycomatrix, graycoprops, hog
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler

def compute_features(args):
    """Robust feature computation with error handling"""
    try:
        filtered_images, label = args
        features = {}
        
        for filter_name, img in filtered_images.items():
            # GLCM Features
            img_uint8 = (img * 255).astype(np.uint8)
            glcm = graycomatrix(img_uint8, [1], [0], 256, symmetric=True)
            features.update({
                f'{filter_name}_contrast': graycoprops(glcm, 'contrast')[0,0],
                f'{filter_name}_energy': graycoprops(glcm, 'energy')[0,0]
            })
            
            # HOG Features
            hog_feat = hog(img, pixels_per_cell=(32,32), cells_per_block=(2,2))
            features[f'{filter_name}_hog_mean'] = hog_feat.mean()
            features[f'{filter_name}_hog_std'] = hog_feat.std()
            
        features['Tumor'] = label
        return features
    except Exception as e:
        print(f"Skipping image due to error: {str(e)[:100]}")
        return None

def create_dataframe(yes_inputs, no_inputs):
    """Create dataframe with progress tracking"""
    with ProcessPoolExecutor() as executor:
        # Submit all tasks
        futures = []
        for img in yes_inputs:
            futures.append(executor.submit(compute_features, (img, 1)))
        for img in no_inputs:
            futures.append(executor.submit(compute_features, (img, 0)))
        
        # Collect results with progress bar
        results = []
        for future in tqdm(as_completed(futures), total=len(futures), 
                         desc="Feature Extraction"):
            result = future.result()
            if result is not None:
                results.append(result)
    
    # Create and validate dataframe
    df = pd.DataFrame(results).dropna()
    if df.empty:
        raise ValueError("No valid features extracted - check input data")
    
    # Normalize features
    scaler = StandardScaler()
    X = scaler.fit_transform(df.drop('Tumor', axis=1))
    df_normalized = pd.DataFrame(X, columns=df.columns[:-1])
    df_normalized['Tumor'] = df['Tumor'].values
    
    return df_normalized.sample(frac=1)