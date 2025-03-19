# src/mpi_genetic_algorithm.py
from mpi4py import MPI
import numpy as np
import time
from src.genetic_algorithms_functions import calculate_fitness, select_in_tournament, order_crossover, mutate, generate_unique_population

def run_parallel_ga(distance_matrix, population_size=10000, num_tournaments=4, 
                    mutation_rate=0.1, num_generations=200, stagnation_limit=5, seed=42):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    np.random.seed(seed + rank)  # Different seed for each process

    num_nodes = distance_matrix.shape[0]
    # Only master process generates the full population.
    if rank == 0:
        population = generate_unique_population(population_size, num_nodes)
    else:
        population = None

    # Broadcast population to all processes.
    population = comm.bcast(population, root=0)
    
    best_fitness_overall = 1e6
    stagnation_counter = 0
    start_time = time.time()
    
    for generation in range(num_generations):
        # Scatter population among processes for fitness evaluation.
        pop_split = np.array_split(population, size)
        local_population = comm.scatter(pop_split, root=0)
        
        # Each process calculates fitness for its local population.
        local_fitness = np.array([calculate_fitness(route, distance_matrix) for route in local_population])
        
        # Gather fitness values at the master.
        fitness_sublists = comm.gather(local_fitness, root=0)
        
        if rank == 0:
            # Combine all fitness values.
            fitness_values = np.concatenate(fitness_sublists)
            current_best = np.min(fitness_values)
            if current_best < best_fitness_overall:
                best_fitness_overall = current_best
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            # Regenerate population if stagnation limit is reached.
            if stagnation_counter >= stagnation_limit:
                print(f"Regenerating population at generation {generation} due to stagnation")
                best_individual = population[np.argmin(fitness_values)]
                population = generate_unique_population(population_size - 1, num_nodes)
                population.append(best_individual)
                stagnation_counter = 0
                # Broadcast updated population to workers.
                population = comm.bcast(population, root=0)
                continue

            # Selection, Crossover, Mutation: performed on the master.
            selected = select_in_tournament(population, fitness_values, number_tournaments=num_tournaments)
            offspring = []
            for i in range(0, len(selected) - 1, 2):
                # Exclude depot for crossover and reattach it.
                child_route = order_crossover(selected[i][1:], selected[i+1][1:])
                offspring.append([0] + child_route)
            mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

            # Replace worst individuals with offspring.
            replace_indices = np.argsort(fitness_values)[-len(mutated_offspring):]
            for idx, new_ind in zip(replace_indices, mutated_offspring):
                population[idx] = new_ind

            # Ensure uniqueness in population.
            unique_population = set(tuple(ind) for ind in population)
            while len(unique_population) < population_size:
                individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
                unique_population.add(tuple(individual))
            population = [list(ind) for ind in unique_population]

            print(f"Generation {generation}: Best fitness = {current_best}")
        else:
            # Other ranks do not perform selection.
            fitness_values = None

        # Broadcast updated population to all processes.
        population = comm.bcast(population, root=0)
    
    if rank == 0:
        total_time = time.time() - start_time
        best_solution = population[np.argmin(np.array([calculate_fitness(route, distance_matrix) for route in population]))]
        print("Best Solution:", best_solution)
        print("Total Distance:", calculate_fitness(best_solution, distance_matrix))
        return total_time
    else:
        return None