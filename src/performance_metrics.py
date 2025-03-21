#src/performance_metrics.py
def calculate_speedup(sequential_time, parallel_time):
    """
    Calculate speedup: sequential_time / parallel_time.
    """
    return sequential_time / parallel_time

def calculate_efficiency(speedup, num_workers):
    """
    Calculate efficiency: speedup / num_workers.
    """
    return speedup / num_workers