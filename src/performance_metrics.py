# performance_metrics.py
def calculate_speedup(sequential_time, parallel_time):
    """
    Calculate the speedup factor.
    
    Parameters:
        - sequential_time (float): Execution time for the sequential version.
        - parallel_time (float): Execution time for the parallel version.
        
    Returns:
        - float: Speedup, defined as sequential_time / parallel_time.
    """
    return sequential_time / parallel_time if parallel_time else float('inf')


def calculate_efficiency(speedup, num_processors):
    """
    Calculate the efficiency of the parallel execution.
    
    Parameters:
        - speedup (float): The measured speedup.
        - num_processors (int): The number of processing units used.
        
    Returns:
        - float: Efficiency (speedup divided by the number of processors).
    """
    return speedup / num_processors if num_processors else 0.0


def amdahl_speedup(sequential_fraction, num_processors):
    """
    Compute the maximum theoretical speedup using Amdahl's Law.
    
    Parameters:
        - sequential_fraction (float): Fraction of the execution that is sequential.
        - num_processors (int): Number of processors used.
        
    Returns:
        - float: Predicted speedup based on Amdahl's Law.
        
    Amdahl's Law: speedup = 1 / (sequential_fraction + (1 - sequential_fraction)/num_processors)
    """
    return 1.0 / (sequential_fraction + (1 - sequential_fraction) / num_processors)


def gustafson_speedup(sequential_fraction, num_processors):
    """
    Compute the predicted speedup using Gustafson's Law.
    
    Parameters:
        - sequential_fraction (float): Fraction of the execution that is sequential.
        - num_processors (int): Number of processors used.
        
    Returns:
        - float: Predicted speedup based on Gustafson's Law.
        
    Gustafson's Law: speedup = num_processors - sequential_fraction * (num_processors - 1)
    """
    return num_processors - sequential_fraction * (num_processors - 1)


if __name__ == "__main__":
    import sys

    # Usage: python performance_metrics.py <sequential_time> <parallel_time> <num_processors> [sequential_fraction]
    if len(sys.argv) < 4:
        print("Usage: python performance_metrics.py <sequential_time> <parallel_time> <num_processors> [sequential_fraction]")
        sys.exit(1)

    sequential_time = float(sys.argv[1])
    parallel_time = float(sys.argv[2])
    num_processors = int(sys.argv[3])
    # Optionally, allow specifying the sequential fraction (default is 0.1)
    sequential_fraction = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1

    speedup = calculate_speedup(sequential_time, parallel_time)
    efficiency = calculate_efficiency(speedup, num_processors)
    amdahl = amdahl_speedup(sequential_fraction, num_processors)
    gustafson = gustafson_speedup(sequential_fraction, num_processors)

    print("Performance Metrics:")
    print(f"  Sequential Time: {sequential_time}")
    print(f"  Parallel Time: {parallel_time}")
    print(f"  Number of Processors: {num_processors}")
    print(f"  Speedup: {speedup:.4f}")
    print(f"  Efficiency: {efficiency:.4f}")
    print(f"  Amdahl's Law Predicted Speedup: {amdahl:.4f}")
    print(f"  Gustafson's Law Predicted Speedup: {gustafson:.4f}")