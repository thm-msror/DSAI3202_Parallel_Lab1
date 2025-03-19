from mpi4py import MPI
import numpy as np
import time
from src.calculate_squares import compute_squares

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Time limit in seconds
time_limit = 300

# Start timing
start_time = time.time()

# Initial value of n
n = int(1e8)  # Start with a reasonable value

# Loop to find the maximum n within the time limit
while True:
    # Split the workload among processes
    chunk_size = n // size
    start_idx = rank * chunk_size
    end_idx = (rank + 1) * chunk_size if rank != size - 1 else n

    # Compute squares for the assigned range
    local_squares = compute_squares(start_idx, end_idx)

    # Gather results at the root process
    squares = comm.gather(local_squares, root=0)

    # Check if time limit is exceeded
    elapsed_time = time.time() - start_time
    if elapsed_time > time_limit:
        break

    # Root process combines results and prints stats
    if rank == 0:
        # Concatenate the results from all processes
        all_squares = np.concatenate(squares)  # Merging all partial results
        print(f"Current n: {n}, Last square: {all_squares[-1]}, Time taken: {elapsed_time:.2f} seconds")

    # Increase n for the next iteration
    n *= 2  # Double n each time (or use a smaller increment if needed)

# Final output from the root process
if rank == 0:
    print(f"Maximum n reached within {time_limit} seconds: {n // 2}")
    print(f"Last square: {all_squares[-1]}")
    print(f"Total time taken: {elapsed_time:.2f} seconds")