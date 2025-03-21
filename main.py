import numpy as np
import pandas as pd
import time
from src.performance_metrics import calculate_speedup, calculate_efficiency
from src.genetic_algorithm_trial import run_genetic_algorithm
from src.genetic_algorithm_pooling import parallel_genetic_algorithm
from src.genetic_algorithm_parallel_improved import parallel_genetic_algorithm_improved  # updated import

def main():
    # Load the distance matrix
    distance_matrix = pd.read_csv('city_distances.csv').to_numpy()

    # GA Parameters
    population_size = 10000
    num_tournaments = 4
    mutation_rate = 0.15
    num_generations = 100
    infeasible_penalty = 1e6
    stagnation_limit = 5
    seed = 42
    early_stopping_threshold = 1100  # Stop early if fitness reaches 1100 or less
    elite_size=5
    convergence_patience=30

    print(" Running Sequential GA...")
    best_distance_seq, sequential_time = run_genetic_algorithm(
        distance_matrix=distance_matrix,
        population_size=population_size,
        num_tournaments=num_tournaments,
        mutation_rate=mutation_rate,
        num_generations=num_generations,
        infeasible_penalty=infeasible_penalty,
        stagnation_limit=stagnation_limit,
        seed=seed
    )

    print("\n Running Parallel GA (Base Multiprocessing)...")
    best_distance_par, parallel_time = parallel_genetic_algorithm(
        distance_matrix=distance_matrix,
        population_size=population_size,
        generations=num_generations,
        mutation_rate=mutation_rate,
        num_tournaments=num_tournaments,
        stagnation_limit=stagnation_limit,
        seed=seed
    )

    print("\n Running Improved Parallel GA (With Elitism + Vectorized + Adaptive)...")
    best_distance_impr, improved_parallel_time = parallel_genetic_algorithm_improved(
        distance_matrix=distance_matrix,
        population_size=population_size,
        generations=num_generations,
        mutation_rate=mutation_rate,
        num_tournaments=num_tournaments,
        stagnation_limit=stagnation_limit,
        early_stopping_threshold=early_stopping_threshold,
        elite_size=elite_size,
        convergence_patience=convergence_patience,
        seed=seed
    )

    # Results Summary
    print("\n Final Best Distances:")
    print(f"   Sequential Best Distance: {best_distance_seq}")
    print(f"   Parallel (Base) Best Distance: {best_distance_par}")
    print(f"   Improved Parallel Best Distance: {best_distance_impr}")

    print("\n Performance Metrics (Base Multiprocessing):")
    speedup = calculate_speedup(sequential_time, parallel_time)
    efficiency = calculate_efficiency(speedup, num_workers=6)
    print(f"  Sequential Execution Time: {sequential_time:.2f} seconds")
    print(f"  Parallel Execution Time: {parallel_time:.2f} seconds")
    print(f"  Speedup: {speedup:.2f}")
    print(f"  Efficiency: {efficiency:.2f}")

    print("\n Performance Metrics (Improved Parallel):")
    speedup = calculate_speedup(sequential_time, improved_parallel_time)
    efficiency = calculate_efficiency(speedup, num_workers=6)
    print(f"  Sequential Execution Time: {sequential_time:.2f} seconds")
    print(f"  Improved Parallel Execution Time: {improved_parallel_time:.2f} seconds")
    print(f"  Speedup: {speedup:.2f}")
    print(f"  Efficiency: {efficiency:.2f}")

if __name__ == "__main__":
    main()
