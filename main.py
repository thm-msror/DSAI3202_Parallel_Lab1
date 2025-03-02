import time
from multiprocessing import cpu_count
from src.data_loader import load_dataset
from src.sequential_version import sequential_execution
from src.parallel_version import parallel_execution
from src.feature_extraction import create_dataframe
from src.model_training import train_and_evaluate

def print_metrics(results):
    """Display formatted metrics for each model."""
    print("\nModel Performance Summary:")
    for model, metrics in results.items():
        print(f"\n{model}:")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1-Score: {metrics['f1']:.4f}")
        print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
        print("Confusion Matrix:")
        print(metrics['confusion_matrix'])

def main():
    # Load dataset
    dataset_path = 'data/brain_tumor_dataset/'
    yes_images, no_images = load_dataset(dataset_path)
    
    # Sequential execution for baseline (optional)
    print("Running sequential version for image filtering...")
    seq_time, yes_seq, no_seq = sequential_execution(yes_images, no_images)
    print(f"Sequential execution time: {seq_time:.2f} seconds")
    
    # Parallel processing for image filtering
    print("\nRunning parallel version for image filtering...")
    par_time, yes_par, no_par = parallel_execution(
        yes_images, no_images,
        max_workers=cpu_count()-1,
        chunk_size=10
    )
    print(f"Parallel execution time: {par_time:.2f} seconds")
    speedup = seq_time / par_time
    efficiency = speedup / (cpu_count()-1)
    print(f"Speedup: {speedup:.2f}x")
    print(f"Efficiency: {efficiency:.2f}")
    
    # Feature extraction
    print("\nCreating feature dataframe...")
    df = create_dataframe(yes_par, no_par)
    print(f"Final dataframe shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage().sum()/1024/1024:.2f} MB")
    
    # Model training and evaluation
    print("\nTraining models...")
    try:
        results = train_and_evaluate(df)
        print_metrics(results)
    except Exception as e:
        print(f"Model training failed due to error: {e}")

if __name__ == "__main__":
    main()
