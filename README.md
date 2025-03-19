# DSAI 3202 – Parallel and Distributed Computing  
## Lecture 6 - Distributed Computing with Python (mpi4py)

### 1. Square Program
- **Objective**: Create a function `square` that computes the square of a series of integers from `1` to `n`.
- **Requirements**:
  - The program must be parallel and use `mpi4py`.
  - Save the Python script as `calculate_squares.py`.
- **Steps**:
  1. **Environment Setup**:
     - Ensure `mpi4py` is installed on all targeted machines.
     - Copy the SSH key from the main machine to the others.
     - Use SSH to access each machine.
  2. **Distribute the Program**:
     - Copy `calculate_squares.py` to each machine in the same directory path or use a shared file system.
     - Create a host file (`machines.txt`) listing the IP addresses of all machines.
  3. **Run the Program**:
     - Execute the program across all machines using:
       ```bash
       mpirun -hostfile machines.txt -np <number_of_processes> python main.py
       ```
  4. **Observe Results**:
     - The root process (rank 0) gathers all partial results, prints the size of the final array of squares, the last square, and the time taken.

### 2. Virus Spread Simulation

#### Objective
Simulate the spread of a virus through a population using MPI.

#### Steps
1. **Initialize the MPI Environment**:
   - Import necessary libraries.
   - Initialize the MPI communicator.
   - Get the rank and size of the current process.

2. **Define Parameters**:
   - Define the population size, chance of virus spread, and generate a random vaccination rate for each process.

3. **Initialize the Population**:
   - Initialize the population array with zeros (uninfected individuals).
   - Infect a small percentage of individuals at the start.

4. **Implement Virus Spread Function**:
   - Create a function to simulate virus spread based on spread chance and vaccination rate.

5. **Simulate Virus Spread**:
   - Iterate over multiple time steps to simulate virus spread.
   - Exchange data between processes using MPI communication.

6. **Calculate Infection Rate**:
   - Calculate the infection rate for each process based on the final infected population count.

7. **Run and Experiment**:
   - Run the program on multiple processors to observe different infection rates.
   - Experiment with changing parameters like spread chance and vaccination rates.

---
