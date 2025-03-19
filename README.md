# DSAI 3202 – Parallel and Distributed Computing  
## Assignment 1 Part 2 - Navigating the City
### Objectives: Develop Python programs that run the uses genetic algorithms in a distributed fashion using MPI4PY or Celery. 

---
## Fleet management using genetic algorithms:  
## Sequential Version
---
Q. Explain the program outlined in the script genetic_algorithm_trial.py. 

**The main overview:**
    - The script `genetic_algorithm_trial.py` implements a Genetic Algorithm (GA) to solve the Fleet Management Problem. 
    - The goal is to find the shortest possible route that visits all cities exactly once and returns to the starting city. 
    - The GA is a heuristic search algorithm inspired by natural selection, which evolves a population of solutions over generations.

**Key steps in the Algorithm:**
1. A unique population of routes is generated using the generate_unique_population function.
Each route starts and ends at the depot (node 0) and is a permutation of the remaining nodes.
2. The fitness of each route is calculated using the calculate_fitness function. 
- The fitness is the negative total distance of the route (since the goal is to minimize distance). 
- A large negative penalty is returned if the route is infeasible (e.g., contains a distance of 10,000).
3. The select_in_tournament function implements tournament selection. 
- It randomly selects a subset of individuals from the population and chooses the one with the best fitness to be a parent for the next generation.
4. The order_crossover function performs order crossover (OX) to create offspring. 
- It combines parts of two-parent routes to produce a new route while preserving the order of cities.
5. The mutate function introduces random changes (swaps) in the route with a probability defined by the mutation rate. 
- This helps maintain genetic diversity in the population.
6. If the algorithm does not improve the best fitness for a specified number of generations (stagnation_limit), the population is regenerated (except for the best individual) to avoid getting stuck in local optima.
7. The algorithm iterates over a fixed number of generations (num_generations). 
In each generation, it evaluates the population's fitness, performs selection, crossover, and mutation, and updates the population.
8. After the loop completes, the best route found and its total distance are printed. 
- The execution time is also recorded and returned.

Q. Run and time the execution of this script.
- ![Sequential run of fleet management using GA](run_sequential.png)
- The execution time for the sequential version of the algorithm (as shown in the output) is 19.8276 seconds. This time may vary depending on the hardware and the size of the distance matrix.
- Stagnation Handling:
    - The algorithm frequently regenerates the population due to stagnation, indicating that it struggles to find better solutions after a few generations. 
    - This suggests that the search space is complex, and the algorithm may benefit from additional optimization techniques.
- Fitness Improvement:
    - The best fitness improves over time, but the improvements are incremental. 
    - The final best fitness is -1800547.0, which corresponds to a total distance of 1,800,547 units.
- Scalability:
    - The algorithm is computationally expensive due to the large population size (10,000) and the number of generations (200). 
    - Parallelization could significantly reduce the execution time.
---
## Parallel Version
