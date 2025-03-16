from mpi4py import MPI
import numpy as np
from src.calculate_squares import compute_squares
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define n (can modify for 1e8 later)
n = 10**6  

# Split workload among processes
chunk_size = n // size
start_idx = rank * chunk_size
end_idx = (rank + 1) * chunk_size if rank != size - 1 else n

# Start timing
start_time = time.time()

# Compute squares for the assigned range
local_squares = compute_squares(start_idx, end_idx)

# Gather results at the root process
squares = comm.gather(local_squares, root=0)

# Root process combines results and prints stats
if rank == 0:
    squares = np.concatenate(squares)
    print(f"Total squares computed: {len(squares)}")
    print(f"Last square: {squares[-1]}")
    print(f"Time taken: {time.time() - start_time:.2f} seconds")