#src/genetic_algorithm_pooling.py
import numpy as np
import time
from itertools import chain
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from src.genetic_algorithms_functions import generate_unique_population
from src.parallel_functions import worker_process, parallel_fitness

def parallel_genetic_algorithm(distance_matrix, population_size=10000, generations=100,
                               mutation_rate=0.1, num_tournaments=5, stagnation_limit=5, seed=42):
    """
    Runs a parallel version of a Genetic Algorithm (GA) for solving the Fleet Management Problem.
    
    The goal is to find the shortest path that visits all cities exactly once and returns to the start.

    Parameters:
        distance_matrix (np.array): 2D matrix containing distances between cities.
        population_size (int): Number of individuals in the population.
        generations (int): Number of generations for which to run the GA.
        mutation_rate (float): Probability of mutating an individual.
        num_tournaments (int): Number of candidates in each tournament selection.
        stagnation_limit (int): Number of stagnant generations allowed before population regeneration.
        seed (int): Random seed for reproducibility.

    Returns:
        tuple: (best_distance, total_time)
            best_distance (float): The total distance of the best solution found.
            total_time (float): Total time taken to run the algorithm.
    """
    
    np.random.seed(seed)
    num_procs = min(cpu_count(), 6)  # Limit to 6 processes max to avoid overloading system
    start_time = time.time()

    # Step 1: Initialize population
    population = np.array(generate_unique_population(population_size, distance_matrix.shape[0]))
    best_solution = None
    best_distance = float('inf')
    best_generation = 0
    stagnation_counter = 0

    # Step 2: Start parallel pool
    with ProcessPoolExecutor(max_workers=num_procs) as executor:
        for gen in range(1, generations + 1):

            # Handle stagnation: Regenerate population if no improvement
            if stagnation_counter >= stagnation_limit:
                print(f"Regenerating population at generation {gen} due to stagnation")
                population = np.array(
                    generate_unique_population(population_size - 1, distance_matrix.shape[0]) + [best_solution]
                )
                stagnation_counter = 0

            # Safety check: ensure correct population size
            if population.shape[0] != population_size:
                population = np.array(
                    generate_unique_population(population_size - 1, distance_matrix.shape[0]) + [best_solution]
                )

            # Step 3: Split population into chunks for parallel workers
            chunks = np.array_split(population, num_procs)
            chunks = [chunk.tolist() for chunk in chunks]  # Convert to lists for multiprocessing

            # Step 4: Submit parallel tasks (each worker handles fitness + selection + crossover + mutation)
            futures = [
                executor.submit(worker_process, chunk, distance_matrix, mutation_rate, num_tournaments)
                for chunk in chunks
            ]
            results = [f.result() for f in futures]  # Wait for all workers to finish

            # Step 5: Collect offspring and fitness values from all workers
            offspring_chunks, fitness_chunks = zip(*results)
            population = np.array(list(chain.from_iterable(offspring_chunks)))  # Flatten offspring

            # Step 6: Re-evaluate fitness of new population (in parallel)
            reeval_chunks = np.array_split(population, num_procs)
            reeval_chunks = [chunk.tolist() for chunk in reeval_chunks]
            fitness_futures = [
                executor.submit(parallel_fitness, chunk, distance_matrix)
                for chunk in reeval_chunks
            ]
            fitness_results = [f.result() for f in fitness_futures]
            fitness_list = list(chain.from_iterable(fitness_results))  # Flatten fitness values
            fitness_array = np.array(fitness_list[:population.shape[0]])

            # Step 7: Track best solution
            gen_best_idx = np.argmin(fitness_array)  # Best = minimum distance
            gen_best_distance = fitness_array[gen_best_idx]
            gen_best_solution = population[gen_best_idx]

            print(f"Generation {gen}: Best calculate_fitness = {gen_best_distance}")

            # Step 8: Update best known solution and handle stagnation
            if gen_best_distance < best_distance:
                best_distance = gen_best_distance
                best_solution = gen_best_solution
                best_generation = gen
                stagnation_counter = 0
            else:
                stagnation_counter += 1

    total_time = time.time() - start_time

    # Final best result
    print(f"\n Best Solution Found (at Generation {best_generation}): {list(best_solution)}")
    print(f" Total Distance: {best_distance}")
    return best_distance, total_time