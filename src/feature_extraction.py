# feature_extraction.py
import numpy as np
import pandas as pd
import skimage.feature as feature
from multiprocessing import Pool, cpu_count

def compute_glcm_features(image, filter_name):
    """
    Computes GLCM (Gray Level Co-occurrence Matrix) features for an image.

    Parameters:
        - image: A 2D array representing the image. Should be in grayscale.
        - filter_name: A string representing the name of the filter applied to the image.

    Returns:
        - features: A dictionary containing the computed GLCM features.
    """
    # Convert the image from float to int
    image = (image * 255).astype(np.uint8)

    # Compute the GLCM
    graycom = feature.graycomatrix(image, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)

    # Compute GLCM properties
    features = {}
    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
        values = feature.graycoprops(graycom, prop).flatten()
        for i, value in enumerate(values):
            features[f'{filter_name}_{prop}_{i+1}'] = value
    return features

def process_single_image(filtered_images, tumor_presence):
    """
    Processes a single image and computes GLCM features.

    Parameters:
        - filtered_images: A dictionary containing filtered images.
        - tumor_presence: An integer (0 or 1) indicating the presence (1) or absence (0) of a tumor.

    Returns:
        - glcm_features: A dictionary containing the GLCM features for the image.
    """
    glcm_features = {}
    for key, image in filtered_images.items():
        glcm_features.update(compute_glcm_features(image, key))
    glcm_features['Tumor'] = tumor_presence
    return glcm_features

def process_images(images_list, tumor_presence):
    """
    Processes a list of images in parallel, applies all filters, computes GLCM features, and adds a "Tumor" key.

    Parameters:
        - images_list: A list of dictionaries, where each dictionary contains filtered images.
        - tumor_presence: An integer (0 or 1) indicating the presence (1) or absence (0) of a tumor.

    Returns:
        - glcm_features_list: A list of dictionaries containing the GLCM features for all filtered images.
    """
    with Pool(cpu_count()) as pool:
        glcm_features_list = pool.starmap(
            process_single_image,
            [(filtered_images, tumor_presence) for filtered_images in images_list]
        )
    return glcm_features_list

def create_dataframe(yes_inputs, no_inputs):
    """
    Combines the GLCM features of 'yes' and 'no' images into a single DataFrame.

    Parameters:
        - yes_inputs: List of processed 'yes' images.
        - no_inputs: List of processed 'no' images.

    Returns:
        - dataframe: A pandas DataFrame containing all GLCM features.
    """
    # Process the 'yes' and 'no' image lists in parallel
    yes_glcm_features = process_images(yes_inputs, 1)
    no_glcm_features = process_images(no_inputs, 0)

    # Combine the features into a single list
    all_glcm_features = yes_glcm_features + no_glcm_features

    # Convert the list of dictionaries to a pandas DataFrame
    dataframe = pd.DataFrame(all_glcm_features)

    # Shuffle the DataFrame
    shuffled_dataframe = dataframe.sample(frac=1).reset_index(drop=True)
    return shuffled_dataframe