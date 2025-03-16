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

# Simulate virus spread over 10 time steps
for t in range(10):
    population = spread_virus(population, spread_chance, vaccination_rate)
    
    if rank != 0:
        comm.send(population, dest=0)  # Send data to root
    else:
        # Root process gathers data from all processes
        all_populations = [population]
        for i in range(1, size):
            received_data = comm.recv(source=i)
            all_populations.append(received_data)
        
        # Combine the populations from all processes
        population = np.sum(all_populations, axis=0)

# Calculate infection rate for each process
total_infected = np.sum(population)
infection_rate = total_infected / population_size
print(f"Process {rank} Infection Rate: {infection_rate:.4f}")