#sec/parallel_functions.py
import numpy as np
import random
from src.genetic_algorithms_functions import calculate_fitness, order_crossover, mutate

def worker_process(chunk, distance_matrix, mutation_rate, num_tournaments):
    """
    Performs fitness evaluation, selection, crossover, and mutation on a chunk of the population.

    This function is designed to run in parallel using multiprocessing. It handles all core steps of the genetic
    algorithm for a subset of the population.

    Parameters:
        chunk (list of list[int]): A subset of the population (each individual is a route).
        distance_matrix (np.ndarray): 2D array representing distances between cities.
        mutation_rate (float): Probability of mutation for each individual.
        num_tournaments (int): Number of individuals to sample in tournament selection.

    Returns:
        tuple:
            - offspring (list of list[int]): New individuals created through crossover and mutation.
            - fitness_values (list[float]): Fitness values (negative distances) for the original individuals.
    """

    # Step 1: Calculate fitness for each individual in the chunk
    # We return negative distances because we are minimizing the distance
    fitness_values = [-calculate_fitness(ind, distance_matrix) for ind in chunk]

    # Step 2: Perform tournament selection to choose individuals for crossover
    selected = []
    for _ in range(len(chunk)):
        # Randomly select num_tournaments individuals and pick the one with the best (lowest) distance
        tournament = np.random.choice(len(chunk), size=num_tournaments, replace=False)
        winner_idx = min(tournament, key=lambda i: fitness_values[i])
        selected.append(chunk[winner_idx])

    # Step 3: Apply order crossover and mutation to generate offspring
    offspring = []
    for i in range(0, len(selected) - 1, 2):
        # Perform order crossover on the inner part of the route (excluding depot 0)
        child = [0] + order_crossover(selected[i][1:], selected[i + 1][1:])
        # Apply mutation to the child
        mutated = mutate(child, mutation_rate)
        offspring.append(mutated)

    # If there is an odd number of selected individuals, mutate the last one directly
    if len(selected) % 2 == 1:
        mutated = mutate(selected[-1], mutation_rate)
        offspring.append(mutated)

    return offspring, fitness_values


def parallel_fitness(chunk, distance_matrix):
    """
    Computes the fitness values for a chunk of individuals in parallel.

    This is a helper function designed for use in parallel re-evaluation of the population's fitness
    after crossover and mutation.

    Parameters:
        chunk (list of list[int]): A subset of the population (each individual is a route).
        distance_matrix (np.ndarray): 2D array representing distances between cities.

    Returns:
        list[float]: A list of negative fitness values (i.e., -total distances) for each route in the chunk.
    """
    return [-calculate_fitness(ind, distance_matrix) for ind in chunk]
