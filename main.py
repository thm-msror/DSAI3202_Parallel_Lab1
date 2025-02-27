# main.py
import time
from src.data_loader import load_dataset
from src.sequential_version import sequential_execution
from src.parallel_version import parallel_execution
from src.feature_extraction import create_dataframe
from src.model_training import split_data, train_and_evaluate_models
from multiprocessing import cpu_count

def main():
    # Load dataset
    dataset_path = 'data/brain_tumor_dataset/'
    yes_images, no_images = load_dataset(dataset_path)
    
    # Sequential execution (for testing)
    print("Running sequential version for 5 images...")
    seq_time = sequential_execution(yes_images, no_images)
    print(f"Sequential execution time: {seq_time:.2f} seconds")
    
    # Parallel execution (for testing)
    print("Running parallel version for 5 images...")
    par_time, yes_results, no_results = parallel_execution(yes_images, no_images, max_workers=cpu_count(), chunk_size=25)
    print(f"Parallel execution time: {par_time:.2f} seconds")
    
    # Calculate speedup and efficiency
    speedup = seq_time / par_time
    efficiency = speedup / cpu_count()
    print(f"Speedup: {speedup:.2f}")
    print(f"Efficiency: {efficiency:.2f}")

    # Feature extraction (Part II)
    print("Creating feature DataFrame...")
    dataframe = create_dataframe(yes_results, no_results)
    print(f"DataFrame shape: {dataframe.shape}")

    # Model training and evaluation (Part III)
    print("Training and evaluating models...")
    X_train, X_test, y_train, y_test = split_data(dataframe)
    results = train_and_evaluate_models(X_train, X_test, y_train, y_test)

    # Print model evaluation results
    for model_name, metrics in results.items():
        print(f"\nModel: {model_name}")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1 Score: {metrics['f1']:.4f}")
        print(f"Confusion Matrix:\n{metrics['confusion_matrix']}")

if __name__ == "__main__":
    main()