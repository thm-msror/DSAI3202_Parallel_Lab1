import numpy as np

def compute_squares(start_idx, end_idx):
    # Generate an array of integers from start_idx to end_idx
    numbers = np.arange(start_idx, end_idx, dtype=np.int64)
    # Compute squares
    squares = numbers ** 2
    return squares