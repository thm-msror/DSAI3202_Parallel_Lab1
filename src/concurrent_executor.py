import time
from concurrent.futures import ProcessPoolExecutor
from src.compute_square import square

def concurrent_execution(numbers):
    """Executes using concurrent.futures ProcessPoolExecutor."""
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(square, numbers))
    end_time = time.time()
    return results, end_time - start_time