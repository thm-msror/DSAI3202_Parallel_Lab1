import time
from src.data_loader import load_dataset
from src.sequential_version import sequential_execution

def main():
    # Load dataset
    dataset_path = 'data/brain_tumor_dataset/'
    yes_images, no_images = load_dataset(dataset_path)
    
    # Sequential execution
    print("Running sequential version...")
    seq_time = sequential_execution(yes_images, no_images)
    print(f"Sequential execution time: {seq_time:.2f} seconds")

if __name__ == "__main__":
    main()