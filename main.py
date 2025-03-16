from mpi4py import MPI
import numpy as np
import time
from src.calculate_squares import compute_squares

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define n (n = 1e8 as required for the assignment)
n = int(1e8)

# Split the workload among processes
chunk_size = n // size
start_idx = rank * chunk_size
end_idx = (rank + 1) * chunk_size if rank != size - 1 else n

# Start timing
start_time = time.time()

# Compute squares for the assigned range
local_squares = compute_squares(start_idx, end_idx)

# Gather results at the root process
# Here we only gather partial results, which minimizes memory overhead
squares = comm.gather(local_squares, root=0)

# Root process combines results and prints stats
if rank == 0:
    # Concatenate the results from all processes
    all_squares = np.concatenate(squares)  # Merging all partial results
    print(f"Total squares computed: {len(all_squares)}")
    print(f"Last square: {all_squares[-1]}")
    print(f"Time taken: {time.time() - start_time:.2f} seconds")