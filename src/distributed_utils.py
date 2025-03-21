# src/distributed_utils.py
import numpy as np
from src.genetic_algorithms_functions import order_crossover, mutate

def vectorized_fitness(route, distance_matrix):
    idx = np.array(route)
    distances = distance_matrix[idx[:-1], idx[1:]]
    total_distance = np.sum(distances) + distance_matrix[idx[-1], idx[0]]
    if 10000 in distances or distance_matrix[idx[-1], idx[0]] == 10000:
        return -1e6
    return -total_distance

def evolve_chunk(chunk, distance_matrix, mutation_rate, num_tournaments=5):
    fitness = [-vectorized_fitness(ind, distance_matrix) for ind in chunk]

    # Selection (handle small chunks)
    selected = []
    for _ in range(len(chunk)):
        tour_size = min(num_tournaments, len(chunk))  # Prevent sampling error
        tour = np.random.choice(len(chunk), tour_size, replace=False)
        winner = min(tour, key=lambda i: fitness[i])
        selected.append(chunk[winner])

    # Crossover + Mutation
    offspring = []
    for i in range(0, len(selected) - 1, 2):
        child = [0] + order_crossover(selected[i][1:], selected[i + 1][1:])
        mutated = mutate(child, mutation_rate)
        offspring.append(mutated)

    if len(selected) % 2 == 1:
        mutated = mutate(selected[-1], mutation_rate)
        offspring.append(mutated)

    return offspring, [-vectorized_fitness(ind, distance_matrix) for ind in offspring]