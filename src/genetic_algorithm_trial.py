import numpy as np
import pandas as pd
import time
from src.genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population

def run_genetic_algorithm(distance_matrix, population_size=10000, num_tournaments=4, 
                          mutation_rate=0.1, num_generations=200, infeasible_penalty=1e6, 
                          stagnation_limit=5, seed=42):
    """
    Runs a Genetic Algorithm (GA) for the Fleet Management Problem

    Parameters:
        distance_matrix (np.array): Distance matrix representing the cities.
        population_size (int): Number of individuals in the population.
        num_tournaments (int): Number of tournaments for selection.
        mutation_rate (float): Probability of mutation.
        num_generations (int): Maximum number of generations.
        infeasible_penalty (float): Penalty for infeasible routes.
        stagnation_limit (int): Number of stagnant generations before regenerating population.
        seed (int): Random seed for reproducibility.

    Returns:
        dict: Best solution, its total distance, and execution time.
    """

    # Generate initial population: each individual is a route starting at node 0
    np.random.seed(seed)  # For reproducibility
    num_nodes = distance_matrix.shape[0]
    population = generate_unique_population(population_size, num_nodes)

    # Initialize variables for tracking stagnation
    best_calculate_fitness = int(1e6)
    stagnation_counter = 0
    
    start_time = time.time() #start timing

    # Main GA loop
    for generation in range(num_generations):
        # Evaluate calculate_fitness
        calculate_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in population])

        # Check for stagnation
        current_best_calculate_fitness = np.min(calculate_fitness_values)
        if current_best_calculate_fitness < best_calculate_fitness:
            best_calculate_fitness = current_best_calculate_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Regenerate population if stagnation limit is reached, keeping the best individual
        if stagnation_counter >= stagnation_limit:
            print(f"Regenerating population at generation {generation} due to stagnation")
            best_individual = population[np.argmin(calculate_fitness_values)]
            population = generate_unique_population(population_size - 1, num_nodes)
            population.append(best_individual)
            stagnation_counter = 0
            continue  # Skip the rest of the loop for this generation

        # Selection, crossover, and mutation
        selected = select_in_tournament(population,
                                        calculate_fitness_values)
        offspring = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            route1 = order_crossover(parent1[1:], parent2[1:])
            offspring.append([0] + route1)
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

        # Replacement: Replace the individuals that lost in the tournaments with the new offspring
        for i, idx in enumerate(np.argsort(calculate_fitness_values)[::-1][:len(mutated_offspring)]):
            population[idx] = mutated_offspring[i]

        # Ensure population uniqueness
        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < population_size:
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        population = [list(individual) for individual in unique_population]

        # Print best calculate_fitness
        print(f"Generation {generation}: Best calculate_fitness = {current_best_calculate_fitness}")

    # Update calculate_fitness_values for the final population
    calculate_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in population])

    # Output the best solution
    best_idx = np.argmin(calculate_fitness_values)
    best_solution = population[best_idx]
    end_time = time.time() #end timing
    print("Best Solution:", best_solution)
    print("Total Distance:", calculate_fitness(best_solution, distance_matrix))
    
    return end_time - start_time