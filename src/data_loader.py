import glob
import cv2

def read_images(images_path):
    """
    Reads all images from a specified path using OpenCV.

    Parameters:
        - images_path (str): The path to the directory containing the images.
    Returns:
        - images (list): A list of images read from the directory.
    """
    images = []
    for file_path in images_path:
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is not None:
            images.append(image)
    return images

def load_dataset(dataset_path):
    """
    Loads the dataset from the given path.

    Parameters:
        - dataset_path (str): Path to the dataset directory.
    Returns:
        - yes_images (list): List of images with tumors.
        - no_images (list): List of images without tumors.
    """
    yes_images = glob.glob(dataset_path + 'yes/*.jpg')
    no_images = glob.glob(dataset_path + 'no/*.jpg')
    
    print(f"Found {len(yes_images)} 'yes' images and {len(no_images)} 'no' images.")  # Debug statement
    
    yes_images = read_images(yes_images)
    no_images = read_images(no_images)
    
    return yes_images, no_images