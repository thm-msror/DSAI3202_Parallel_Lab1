import numpy as np

# Virus spread function
def spread_virus(population, spread_chance, vaccination_rate):
    new_population = population.copy()
    for i in range(len(population)):
        if population[i] == 1:  # If infected
            for j in range(len(population)):
                if population[j] == 0 and np.random.rand() < spread_chance * (1 - vaccination_rate):
                    new_population[j] = 1  # Infecting the person
    return new_population