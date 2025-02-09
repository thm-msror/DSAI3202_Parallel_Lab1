# This is Lab2 of DSAI3202 - First Parallel Programs.
---

### 1. Objectives  
- Build a first program using **threads** in Python.  
- Build a first program using **processes** in Python.  

---

### 2. Tasks  

#### 2.a. The Sequential Case  
a. Make a function that randomly generates **1000 characters** and joins them.  
b. Make a function that randomly generates **1000 numbers** and adds them.  
c. Time the execution of the two functions.  

#### 2.b. Threading  
a. Create a **thread** for each of the functions. Run them and time the execution.  
b. **Advanced work**: Create **two threads per function**.  

#### 2.c. Processes  
a. Create a **process** for each of the functions. Run them and time the execution.  
b. **Advanced work**: Create **two threads per function**.  

#### 2.d. Performance Analysis  
For each case, compute:  
1. The **speedup**.  
2. The **efficiency**.  
3. The speedups using **Amdahl’s Law**.  
4. The speedups using **Gustafson’s Law**.  

#### 2.e. Conclusions  
- Summarize your findings and conclusions based on the performance analysis.  

---
#### Parallel Fraction (P) Calculation  
To calculate the parallel fraction \( P \) of the program:  
1. Count the total number of lines in the program, excluding:  
   - Imports  
   - Function definitions (`def`)  
   - Function return statements  
   - Comments  
   - Empty lines

2. Calculate the parallel lines of code:  
   - **Parallel fraction (P)**:  
     \[
     P = \frac{\text{Parallel lines}}{\text{Total lines}}
     \]

---

#### Performance Findings  
1. **Initial Implementation**:  
   - Initially, the program used **one thread** and **one process** for each function.  
   - The performance was **suboptimal** because the functionality of threads and processes was not fully utilized.  

2. **Optimized Implementation**:  
   - To improve performance, the data was divided, and **multiple threads and processes** were created to handle the data in parallel.  
   - This follows the **MIMD (Multiple Instruction, Multiple Data)** and **SIMD (Single Instruction, Multiple Data)** paradigms from Flynn's Taxonomy.  

3. **Key Observations**:  
   - **Threading**:  
     - Threading showed **limited speedup** for CPU-bound tasks due to Python's **Global Interpreter Lock (GIL)**.  
     - Efficiency was **low**, as expected for CPU-bound tasks.  
   - **Multiprocessing**:  
     - Multiprocessing provided a **significant speedup** for CPU-bound tasks by bypassing the GIL.  
     - Efficiency was **higher** compared to threading, but there was still some overhead from process creation and communication.  

4. **Theoretical Predictions**:  
   - **Amdahl’s Law** and **Gustafson’s Law** were used to predict the theoretical speedup.  
   - The actual speedup for multiprocessing was **close to the theoretical predictions**, indicating effective parallelization.  

---

