# src/parallel_functions_improved.py

import numpy as np
import random
from src.genetic_algorithms_functions import order_crossover, mutate

def vectorized_fitness(route, distance_matrix):
    """
    Compute the total distance of a given route using vectorized NumPy operations.
    
    Parameters:
        route (list[int]): The sequence of city indices representing the route.
        distance_matrix (np.ndarray): 2D matrix of distances between cities.

    Returns:
        float: The negative total distance of the route (penalized with -1e6 for infeasible paths).
               A negative value is used because the algorithm is designed to maximize fitness,
               so minimizing distance means maximizing the negative distance.
    """
    idx = np.array(route)
    
    # Calculate the distances between consecutive cities
    distances = distance_matrix[idx[:-1], idx[1:]]
    
    # Total route distance includes return to the starting city (depot)
    total_distance = np.sum(distances) + distance_matrix[idx[-1], idx[0]]
    
    # Apply penalty for infeasible edges (i.e., distance == 10000)
    if 10000 in distances or distance_matrix[idx[-1], idx[0]] == 10000:
        return -1e6

    return -total_distance  # Negated for minimization through maximization


def worker_process(chunk, distance_matrix, mutation_rate, num_tournaments):
    """
    Worker function for parallel execution of GA operations on a chunk of the population.

    This function evaluates fitness, performs tournament selection, applies crossover and mutation,
    and returns the generated offspring.

    Parameters:
        chunk (list[list[int]]): Subset of population assigned to this process.
        distance_matrix (np.ndarray): 2D matrix of distances between cities.
        mutation_rate (float): Probability of applying mutation to a child.
        num_tournaments (int): Number of individuals to include in each tournament for selection.

    Returns:
        tuple:
            offspring (list[list[int]]): New population of children after crossover and mutation.
            fitness_values (list[float]): List of fitness scores (negative distances) for original individuals.
    """
    # Step 1: Evaluate fitness for the current chunk
    fitness_values = [-vectorized_fitness(ind, distance_matrix) for ind in chunk]

    # Step 2: Tournament selection to choose parents
    selected = []
    for _ in range(len(chunk)):
        # Randomly choose a subset and pick the best (minimum distance)
        tournament = np.random.choice(len(chunk), size=num_tournaments, replace=False)
        winner_idx = min(tournament, key=lambda i: fitness_values[i])
        selected.append(chunk[winner_idx])

    # Step 3: Apply crossover and mutation to generate offspring
    offspring = []
    for i in range(0, len(selected) - 1, 2):
        parent1, parent2 = selected[i], selected[i + 1]
        child = [0] + order_crossover(parent1[1:], parent2[1:])
        mutated = mutate(child, mutation_rate)
        offspring.append(mutated)

    # Step 4: Handle odd-length population by mutating the last individual directly
    if len(selected) % 2 == 1:
        mutated = mutate(selected[-1], mutation_rate)
        offspring.append(mutated)

    return offspring, fitness_values


def parallel_fitness(chunk, distance_matrix):
    """
    Parallelized fitness evaluation for a chunk of individuals.

    Parameters:
        chunk (list[list[int]]): List of individuals (routes) to evaluate.
        distance_matrix (np.ndarray): 2D matrix of distances between cities.

    Returns:
        list[float]: Fitness scores (negative distances) for each individual in the chunk.
    """
    return [-vectorized_fitness(ind, distance_matrix) for ind in chunk]