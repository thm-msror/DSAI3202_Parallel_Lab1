# DSAI 3202 – Parallel and Distributed Computing  

## Assignment 1 Part 2 - Navigating the City

### Objectives: Develop Python programs that run the uses genetic algorithms in a distributed fashion using MPI4PY or Celery

---

## Fleet management using genetic algorithms  

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

- The fitness is the total distance of the route (the goal is to minimize distance).
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
- The execution time for the sequential version of the algorithm (as shown in the output) is 19.6252 seconds. This time may vary depending on the hardware and the size of the distance matrix.
- Stagnation Handling:
  - The algorithm frequently regenerates the population due to stagnation, indicating that it struggles to find better solutions after a few generations.
  - This suggests that the search space is complex, and the algorithm may benefit from additional optimization techniques.
- Fitness Improvement:
  - The best fitness improves over time, but the improvements are incremental:
    - Initially, the best fitness is 1395.0 (Generation 0).
    - After the first regeneration at Generation 5, the best fitness improves to 1278.0 (Generation 6).
    - Later, at Generation 92, the best fitness further improves to 1224.0, which remains the best solution until the end of the run.
  - The final best fitness is 1224.0, which corresponds to a total distance of 1224 units.
- Scalability:
  - The algorithm is computationally expensive due to the large population size (10,000) and the number of generations (200).
  - Parallelization could significantly reduce the execution time.

---

## Parallel Version (Using Multiprocessing)

6. Parallelize the code (20 pts)
After running the code sequentially, the current part of the assignment requires you to run the code in parallel using multiprocessing.

- Define the parts to be parallelized, explain your choices

1. **Fitness Calculation**: Each individual's fitness is computed independently, making it ideal for parallel processing.
2. **Selection**: Tournament selection can be performed concurrently across different subsets of the population.
3. **Crossover & Mutation**: These genetic operations are applied to selected parents independently, allowing for parallel execution.
4. **Re-evaluation**: After generating new offspring, their fitness evaluations can be parallelized.

- Parallelize your program using multiprocessing.
We employed Python’s `concurrent.futures.ProcessPoolExecutor` to distribute tasks across multiple processes. The key steps include:
- **Chunking the Population**: The population is divided into smaller chunks, each processed by a separate worker.
- **Worker Function**: Each worker computes fitness, performs selection, crossover, and mutation on its assigned chunk.
- **Parallel Execution**: The main process submits tasks to the executor, which distributes them among the available worker processes.

- **Below is a critical section of the parallel implementation:**

```python
 # Step 2: Start parallel pool
    with ProcessPoolExecutor(max_workers=num_procs) as executor:
        for gen in range(1, generations + 1):

            # Handle stagnation: Regenerate population if no improvement
            if stagnation_counter >= stagnation_limit:
                print(f"Regenerating population at generation {gen} due to stagnation")
                population = np.array(
                    generate_unique_population(population_size - 1, distance_matrix.shape[0]) + [best_solution]
                )
                stagnation_counter = 0

            # Safety check: ensure correct population size
            if population.shape[0] != population_size:
                population = np.array(
                    generate_unique_population(population_size - 1, distance_matrix.shape[0]) + [best_solution]
                )

            # Step 3: Split population into chunks for parallel workers
            chunks = np.array_split(population, num_procs)
            chunks = [chunk.tolist() for chunk in chunks]  # Convert to lists for multiprocessing

            # Step 4: Submit parallel tasks (each worker handles fitness + selection + crossover + mutation)
            futures = [
                executor.submit(worker_process, chunk, distance_matrix, mutation_rate, num_tournaments)
                for chunk in chunks
            ]
            results = [f.result() for f in futures]  # Wait for all workers to finish

            # Step 5: Collect offspring and fitness values from all workers
            offspring_chunks, fitness_chunks = zip(*results)
            population = np.array(list(chain.from_iterable(offspring_chunks)))  # Flatten offspring
```

- `from itertools import chain flattens the list of lists efficiently, it’s used to:`
  - Merge the offspring returned from multiple worker processes
  - Merge their fitness scores into one array
  - This ensures the next generation operates on a clean, unified population.
  - Added due to the scalar array and index out of bound errors.

- **ProcessPoolExecutor:** Manages a pool of worker processes to which tasks can be submitted. It handles the distribution of tasks and collection of results.
- **Chunking the Population:** The population is split into smaller subsets (chunks), each assigned to a different worker process. This division enables parallel processing of these subsets, improving efficiency.
- **Submitting Tasks:** For each chunk, a task is submitted to the executor. The worker_process function is called with the chunk and other necessary parameters. Each worker operates independently, performing fitness evaluation, selection, crossover, and mutation on its assigned chunk.
- **Collecting Results:** Once all tasks are completed, the main process collects the results (new offspring and their fitness values) from all workers and combines them to form the updated population.

- Run your code and compute the performance metrics.
  - ![Performance metrics for initial run of multiprocessing](initial_mp_metrics.png)
  - **Solution Quality:** The parallel implementation discovered a better solution (distance of 1112.0) compared to the sequential version (distance of 1224.0). This improvement is likely due to increased exploration facilitated by parallel processing.
  - **Execution Time:** Despite parallelization, the execution time increased. This outcome can be attributed to:
    - Inter-process Communication Overhead: Transferring data between processes incurs additional time.
    - Memory Transfer Costs: Large data structures, such as the distance matrix and population, require significant resources to share among processes.
    - Process Management Overhead: Initiating and managing multiple processes introduces additional computational overhead.

7. Enhance the algorithm (20 pts).
There are several improvements that can be implemented in the algorithm.

- What improvements do you propose? Add them to your code.

  - Elitism: Retains best individuals across generations.
  - Adaptive mutation rate: Mutation decreases as generations progress.
  - Early stopping: Stops if a satisfactory solution is found.
  - Convergence detection: Stops if no significant improvement in recent generations.
  - Vectorized fitness: Uses fast NumPy operations to compute distances.

| Problem in Base Version                          | Solution in Improved Version                                                                                   |
|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| High overhead in fitness calculation             | Used `vectorized_fitness()` to minimize per-individual computation                                         |
| Fixed mutation rate led to early stagnation      | Introduced `adaptive mutation rate` to maintain diversity early and reduce noise later                     |
| No protection for best solutions                 | Implemented `elitism` to ensure best individuals are preserved across generations                          |
| Only stagnation used for early exit              | Added `early convergence detection` (based on no improvement over X generations) + early stopping threshold |
| Execution time was long despite parallelism      | Reduced overhead by combining operations in `worker_process()` and avoiding large shared memory transfers   |

- After adding your improvements, recompute the performance metrics and compare with before the enhancements.

  - ![Performance metrics for improved run of multiprocessing](improved_mp_metrics.png)
  - The base multiprocessing version produced better routes than the sequential version but suffered from overhead and communication latency.
  - The improved version achieved the best of both worlds:
    - Higher-quality solutions (lowest route distance)
    - Faster execution (more than 2x faster than base parallel)
  - These improvements make the algorithm scalable, robust, and efficient for larger problem sizes.

---

## Parallel Version (Using Distributed mpi4py)

6. Parallelize the code
After running the code sequentially and with multiprocessing, the current part of the assignment requires you to run the code in parallel over multiple machines.

- Define the parts to be distributed and parallelized, explain your choices
  - The **Genetic Algorithm (GA)** process was broken down into the following components:
    - **Population Initialization**: Only done by Rank 0.
    - **Fitness Evaluation**: The most computationally intensive part, distributed across all machines.
    - **Selection, Crossover, Mutation**: Performed locally on each node for their assigned population chunk.
    - **Best Individual Gathering**: Each node computes its local best, which is sent to Rank 0 to identify the global best.
    - **Broadcasting the Best**: Rank 0 broadcasts the current global best individual and its fitness to all nodes.
    - **Early Stopping**: Triggered on Rank 0 and broadcast to all nodes based on stagnation threshold.

**Why these parts?**

- Fitness evaluation is the bottleneck, so parallelizing it significantly reduces execution time.
- Selection, crossover, and mutation are local operations that can run independently on each machine.
- Aggregating global best ensures global convergence while preserving decentralization for speed.

- Parallelize your program
The code was modified to use `mpi4py` as follows:

- Used `MPI.COMM_WORLD` to identify each process by rank and split the total population.
- Rank 0:
  - Initializes the full population.
  - Distributes equal chunks to all ranks using `comm.scatter`.
  - Gathers best individuals from all ranks using `comm.gather` and evaluates the global best.
  - Broadcasts best results to all ranks.
- All Ranks:
  - Receive their chunk of population.
  - Perform local fitness evaluation and genetic operations (selection, crossover, mutation).
  - Share results with Rank 0 using `comm.gather` and `comm.allgather`.

The main distributed GA logic is encapsulated in:

- `src/genetic_algorithm_distributed.py` — Handles all MPI-based coordination and computation.
- `src/distributed_utils.py` — Contains fitness and evolution logic (vectorized for speed).

Synchronization:

- `comm.Barrier()` ensures all nodes terminate cleanly to avoid hanging processes.

DeprecationWarnings were silenced using Python’s `warnings` module for clean output.

- Run your code and compute the performance metrics
To run the distributed version on multiple machines with `mpi4py`:

```bash
mpirun -hostfile machines.txt -n 24 python main_distributed.py
```

- Each machine contributed 6 processes (cores). The hostfile machines.txt included 4 machines, totaling 24 MPI processes.
  - ![Performance metrics for initial run of sequential and multiprocessing using extended city map](extended_metrics.png)
  - Ran correclty for the first run, after which it kept providing numpy core outdated errors and warning, due to one of the machines.
  - Therefore, we reduced the machines to 3, including mine, and changed the n to 12, for the improved run below.

7. Enhance the algorithm
There are several improvements that can be implemented in the algorithm.

- Distribute your algorithm over 2 machines or more
  - Final distribution command:

  ```bash
  mpirun -hostfile machines.txt -n 12 python main_distributed.py
  ```

- What improvements do you propose? Add them to your code
While these enhancements worked well in the **sequential** and **multiprocessing** versions, they were **not retained in the final distributed implementation** due to the following issues:

| Improvement Tried                  | Result                                                                 |
|-----------------------------------|------------------------------------------------------------------------|
| Adaptive Mutation Rate            | Slower runtime due to mutation-rate syncing across all MPI processes   |
| Early Stopping by Fitness Average | Caused premature termination, limiting exploration in parallel setting |
| Stagnation + Avg Fitness Check    | No measurable improvement in performance or path quality               |

### Improvements added were

**Stagnation-Based Early Stopping**  
A simple early stopping mechanism based on no improvement over `stagnation_limit` generations was retained to prevent unnecessary iterations.
**`comm.Barrier()` for Clean Termination**  
Ensured all MPI processes terminate gracefully — fixing the hanging terminal issue observed in early runs.

- After adding your improvements, recompute the performance metrics and compare with before the enhancements
  - ![Improved performance metrics for distributed run](improved_distributed_metrics.png)
  - Since, only minimum improvements were added, we do not see a significant change, except for effeciency.

---

## Large scale problem (10 pts)

- Run the program using the extended city map: city_distances_extended.csv. Successful execution in feasible time.
  - ![Improved performance metrics for distributed run](extended_metrics.png)

- How would you add more cars to the problem?
1. Implementing Multiple Vehicles:
- Incorporating multiple vehicles transforms the problem into the Capacitated Vehicle Routing Problem (CVRP), where each vehicle has a capacity constraint, and the goal is to minimize the total distance traveled while servicing all customers.​

a. Problem Formulation:
- Capacity Constraints: Each vehicle has a maximum load it can carry, and each customer has a specific demand. 
- The sum of demands in any vehicle's route should not exceed its capacity.​

b. Genetic Representation:
- Chromosome Structure: Represent each chromosome as a sequence of routes, where each route corresponds to a vehicle's path starting and ending at the depot (node 0).
- For example, a chromosome could be represented as [[0, 2, 5, 0], [0, 3, 4, 0], [0, 1, 6, 0]], indicating three routes for three vehicles.​

c. Fitness Evaluation:
- Fitness Function: Calculate the total distance traveled by all vehicles. 
- If any vehicle's route exceeds its capacity, apply a penalty to the fitness score to discourage infeasible solutions.​

d. Genetic Operators:
- Crossover: Design crossover operators that exchange sub-routes between parent chromosomes while maintaining feasibility concerning vehicle capacities.​
- Mutation: Implement mutation operators that adjust routes by reassigning customers between vehicles or altering the sequence of visits within a route.​

e. Initialization:
- Clustering Techniques: Use clustering methods (e.g., k-means) to group geographically close customers, assigning each cluster to a vehicle. 
- This approach provides a good starting point for the GA.

---
