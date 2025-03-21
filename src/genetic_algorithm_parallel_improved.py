# src/genetic_algorithm_parallel_improved.py

import numpy as np
import time
from itertools import chain
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from src.genetic_algorithms_functions import generate_unique_population
from src.parallel_functions_improved import worker_process, parallel_fitness, vectorized_fitness


def parallel_genetic_algorithm_improved(
        distance_matrix, 
        population_size=20000, 
        generations=100,
        mutation_rate=0.2, 
        num_tournaments=5, 
        stagnation_limit=10,
        early_stopping_threshold=None, 
        elite_size=5, 
        convergence_patience=10, 
        seed=42):
    """
    Parallel Genetic Algorithm with enhancements for solving the Fleet Management Problem.

    Enhancements:
        Elitism: Retains best individuals across generations.
        Adaptive mutation rate: Mutation decreases as generations progress.
        Early stopping: Stops if a satisfactory solution is found.
        Convergence detection: Stops if no significant improvement in recent generations.
        Vectorized fitness: Uses fast NumPy operations to compute distances.

    Parameters:
        distance_matrix (np.ndarray): Distance matrix between cities.
        population_size (int): Total number of individuals in the population.
        generations (int): Total number of generations to evolve.
        mutation_rate (float): Initial mutation rate (decays over time).
        num_tournaments (int): Tournament size used for parent selection.
        stagnation_limit (int): Number of stagnant generations before resetting population.
        early_stopping_threshold (float): Stops early if this distance or better is reached.
        elite_size (int): Number of top individuals preserved each generation.
        convergence_patience (int): Number of generations to check for convergence.
        seed (int): Seed for reproducibility.

    Returns:
        tuple:
            - best_distance (float): Best distance (fitness) found.
            - total_time (float): Execution time in seconds.
    """

    # Seed RNG and track time
    np.random.seed(seed)
    start_time = time.time()
    num_procs = min(cpu_count(), 6)

    # Generate initial population of routes
    population = np.array(generate_unique_population(population_size, distance_matrix.shape[0]))

    # Initialize tracking variables
    best_solution = None
    best_distance = float('inf')
    best_generation = 0
    stagnation_counter = 0
    fitness_history = []

    # Begin parallel processing
    with ProcessPoolExecutor(max_workers=num_procs) as executor:
        for gen in range(1, generations + 1):
            
            # Regenerate population if stagnation detected
            if stagnation_counter >= stagnation_limit:
                print(f"Regenerating population at generation {gen} due to stagnation")
                population = np.array(
                    generate_unique_population(population_size - 1, distance_matrix.shape[0]) + [best_solution]
                )
                stagnation_counter = 0

            # Ensure correct population size
            if population.shape[0] != population_size:
                population = np.array(
                    generate_unique_population(population_size - 1, distance_matrix.shape[0]) + [best_solution]
                )

            # Calculate current fitness and select elites
            fitness_values = np.array([-vectorized_fitness(ind, distance_matrix) for ind in population])
            elite_indices = np.argsort(fitness_values)[:elite_size]
            elites = [population[i] for i in elite_indices]

            # Decaying mutation rate: more exploration early, more exploitation later
            current_mutation_rate = max(0.05, mutation_rate * (1 - gen / generations))

            # Divide population into chunks for multiprocessing
            chunks = np.array_split(population, num_procs)
            chunks = [chunk.tolist() for chunk in chunks]

            # Submit jobs for each chunk to perform selection + crossover + mutation
            futures = [
                executor.submit(worker_process, chunk, distance_matrix, current_mutation_rate, num_tournaments)
                for chunk in chunks
            ]
            results = [f.result() for f in futures]

            # Combine offspring from all workers
            offspring_chunks, _ = zip(*results)
            population = np.array(list(chain.from_iterable(offspring_chunks)))

            # Evaluate fitness for new population (in parallel)
            reeval_chunks = np.array_split(population, num_procs)
            reeval_chunks = [chunk.tolist() for chunk in reeval_chunks]
            fitness_futures = [executor.submit(parallel_fitness, chunk, distance_matrix) for chunk in reeval_chunks]
            fitness_results = [f.result() for f in fitness_futures]
            fitness_list = list(chain.from_iterable(fitness_results))
            fitness_array = np.array(fitness_list[:population.shape[0]])

            # Add elites back into the population
            population = np.concatenate([population, elites])
            elite_fitness = np.array([-vectorized_fitness(ind, distance_matrix) for ind in elites])
            fitness_array = np.concatenate([fitness_array, elite_fitness])

            # Track generation's best individual
            gen_best_idx = np.argmin(fitness_array)
            gen_best_distance = fitness_array[gen_best_idx]
            gen_best_solution = population[gen_best_idx]
            fitness_history.append(gen_best_distance)

            print(f"Generation {gen}: Best Distance = {gen_best_distance}")

            # Update best overall solution
            if gen_best_distance < best_distance:
                best_distance = gen_best_distance
                best_solution = gen_best_solution
                best_generation = gen
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            # Stop if desired solution quality reached
            if early_stopping_threshold and best_distance <= early_stopping_threshold:
                print(f"Early stopping at generation {gen} with best distance {best_distance}")
                break

            # Convergence check: no improvement over N generations
            if len(fitness_history) >= convergence_patience:
                improvements = np.diff(fitness_history[-convergence_patience:])
                if np.all(np.abs(improvements) < 1.0):
                    print(f"Early convergence at generation {gen}. No significant improvement.")
                    break

    total_time = time.time() - start_time

    # Output final result
    print(f"\nBest Solution Found (Generation {best_generation}): {list(best_solution)}")
    print(f"Total Distance: {best_distance}")
    return best_distance, total_time