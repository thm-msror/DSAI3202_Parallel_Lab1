import numpy as np

def spread_virus(population, spread_chance, vaccination_rate):
    new_population = population.copy()
    for i in range(len(population)):
        if population[i] == 1:  # If infected
            # Infect only a few neighbors (not the entire population)
            neighbors = np.random.choice(len(population), size=5, replace=False)  # Infect 5 random individuals
            for j in neighbors:
                if population[j] == 0 and np.random.rand() < spread_chance * (1 - vaccination_rate):
                    new_population[j] = 1  # Infect the person
    return new_population