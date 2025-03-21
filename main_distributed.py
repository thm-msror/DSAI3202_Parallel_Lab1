from mpi4py import MPI
import numpy as np
import pandas as pd
import time

from src.performance_metrics import calculate_speedup, calculate_efficiency
from src.genetic_algorithm_distributed import run_distributed_ga
from src.genetic_algorithm_trial import run_genetic_algorithm

def main_distributed():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # Parameters
    population_size = 10000
    num_tournaments = 4
    mutation_rate = 0.15
    num_generations = 100
    infeasible_penalty = 1e6
    stagnation_limit = 5
    seed = 42

    # Load data (rank 0 only)
    if rank == 0:
        print("Running Sequential GA on Rank 0...")
        distance_matrix = pd.read_csv("city_distances.csv").to_numpy()
        
        best_seq_dist, seq_time = run_genetic_algorithm(
            distance_matrix=distance_matrix,
            population_size=population_size,
            num_tournaments=num_tournaments,
            mutation_rate=mutation_rate,
            num_generations=num_generations,
            infeasible_penalty=infeasible_penalty,
            stagnation_limit=stagnation_limit,
            seed=seed
        )

        print(f" Sequential Best Distance: {best_seq_dist}")
        print(f" Sequential Time: {seq_time:.2f} seconds")

    else:
        distance_matrix = None
        seq_time = None

    # Broadcast matrix and seq_time to all ranks
    distance_matrix = comm.bcast(distance_matrix, root=0)
    seq_time = comm.bcast(seq_time, root=0)

    # Run distributed GA
    print(f" Rank {rank} starting distributed GA...")
    dist_best_distance, dist_time = run_distributed_ga(distance_matrix)

    # Rank 0 shows final results
    if rank == 0:
        print("\n Final Best Distances and Times")
        print(f"  Sequential Best Distance: {best_seq_dist}")
        print(f"  Sequential Time: {seq_time:.2f} seconds")
        print(f"  Final Best Distance (Distributed):  {dist_best_distance}")
        print(f"  Distributed Execution Time: {dist_time:.2f} seconds")

        print("\n Performance Metrics (Distributed vs Sequential):")
        speedup = calculate_speedup(seq_time, dist_time)
        efficiency = calculate_efficiency(speedup, comm.Get_size())
        print(f" Speedup: {speedup:.2f}")
        print(f" Efficiency: {efficiency:.2f}")

if __name__ == "__main__":
    main_distributed()
