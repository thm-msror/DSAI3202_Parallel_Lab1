# src/genetic_algorithm_distributed.py
from mpi4py import MPI
import numpy as np
import time
from src.genetic_algorithms_functions import generate_unique_population
from src.distributed_utils import evolve_chunk, vectorized_fitness

def run_distributed_ga(distance_matrix, population_size=10000, generations=100,
                       mutation_rate=0.2, num_tournaments=5, elite_size=3,
                       stagnation_limit=10, seed=42):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    np.random.seed(seed + rank)
    chunk_size = population_size // size
    if rank == 0:
        full_population = generate_unique_population(population_size, distance_matrix.shape[0])
        chunks = [full_population[i * chunk_size:(i + 1) * chunk_size] for i in range(size)]
    else:
        chunks = None

    local_population = comm.scatter(chunks, root=0)
    best_solution = None
    best_distance = float('inf')
    stagnation = 0

    if rank == 0:
        start_time = time.time()

    for gen in range(generations):
        offspring, local_fitness = evolve_chunk(local_population, distance_matrix, mutation_rate, num_tournaments)
        best_local_idx = np.argmin(local_fitness)
        best_local_fitness = local_fitness[best_local_idx]
        best_local_solution = offspring[best_local_idx]

        global_best_fitness = comm.allgather(best_local_fitness)
        global_best_solution = comm.gather(best_local_solution, root=0)

        if rank == 0:
            min_idx = np.argmin(global_best_fitness)
            global_best = global_best_fitness[min_idx]
            if global_best < best_distance:
                best_distance = global_best
                best_solution = global_best_solution[min_idx]
                stagnation = 0
            else:
                stagnation += 1
            print(f"Generation {gen}: Best Distance = {best_distance}")

        best_distance = comm.bcast(best_distance, root=0)
        best_solution = comm.bcast(best_solution, root=0)

        if stagnation >= stagnation_limit:
            if rank == 0:
                print(f"Early stopping at generation {gen}")
            break

        local_population = offspring

    if rank == 0:
        total_time = time.time() - start_time
        return best_distance, total_time
    else:
        return None, None
