import numpy as np
import pandas as pd
import time
from src.genetic_algorithms_functions import calculate_fitness, select_in_tournament, order_crossover, mutate, generate_unique_population
from src.performance_metrics import calculate_speedup, calculate_efficiency, amdahl_speedup, gustafson_speedup
from src.genetic_algorithm_trial import run_genetic_algorithm

def main():
    # Load the distance matrix
    distance_matrix = pd.read_csv('city_distances.csv').to_numpy()
    
    # Parameters
    population_size = 10000
    num_tournaments = 4
    mutation_rate = 0.1
    num_generations = 200
    infeasible_penalty = 1e6
    stagnation_limit = 5
    
    # Run the genetic algorithm sequentially
    sequential_time = run_genetic_algorithm(distance_matrix, population_size, num_tournaments,
                                            mutation_rate, num_generations, infeasible_penalty,
                                            stagnation_limit)
    
    # Print results
    print("Performance Metrics:")
    print(f"  Sequential Time: {sequential_time:.4f} seconds")

if __name__ == "__main__":
    main()