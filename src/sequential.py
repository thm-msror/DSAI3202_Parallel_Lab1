import time
from src.compute_square import square

def sequential_execution(numbers):
    """Computes the squares sequentially."""
    start_time = time.time()
    results = [square(n) for n in numbers]
    end_time = time.time()
    return results, end_time - start_time