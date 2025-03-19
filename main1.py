from mpi4py import MPI
import numpy as np
from src.virus_spread import spread_virus

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define parameters
population_size = 1000
spread_chance = 0.3  # Probability of spread
vaccination_rate = np.random.uniform(0.1, 0.5)  # Random vaccination rate for each process

# Initialize population
population = np.zeros(population_size, dtype=int)  # 0 for uninfected, 1 for infected

# Rank 0 will initialize the infections
if rank == 0:
    infected_indices = np.random.choice(population_size, int(0.1 * population_size), replace=False)
    population[infected_indices] = 1  # Infect 10% of the population

# Broadcast the initial population from rank 0 to all processes
population = comm.bcast(population, root=0)

# Simulate virus spread over 10 time steps
for t in range(10):
    population = spread_virus(population, spread_chance, vaccination_rate)
    
    # Gather all populations at rank 0
    all_populations = comm.gather(population, root=0)
    
    if rank == 0:
        # Combine the populations from all processes
        combined_population = np.zeros_like(population)
        for p in all_populations:
            combined_population = np.logical_or(combined_population, p).astype(int)
        population = combined_population
    
    # Broadcast the updated population back to all processes
    population = comm.bcast(population, root=0)

# Calculate infection rate for each process
total_infected = np.sum(population)
infection_rate = total_infected / population_size
print(f"Process {rank} Infection Rate: {infection_rate:.4f}")