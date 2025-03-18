# DSAI 3202 – Parallel and Distributed Computing  
## Assignment 1 Part 1 - Multiprocessing 
### Objectives: Develop Python programs that take advantage of Python's multiprocessing capabilities.
---

## Square Program
- Create a function `square` that computes the square of an integer.
- Create a list of 10<sup>6</sup> numbers.
- Time the program in these scenarios on the random list:
    - A sequential for loop.
    - A multiprocessing for loop with a process for each number.
    - A multiprocessing pool with both `map()` and `apply()`.
    - A `concurrent.futures` `ProcessPoolExecutor`.
- What are your conclusions?
    - The multiprocessing loop program creating a process for each number crashes the first time with a memory error and gets killed upon subsequent executions if we try to run the program again.
    - ![Memory error caused due to multiprocessing loop for each number](memory_error.png)
    - ![Program Killed Shown due to multiprocessing loop for each number](killed_error.png)
    - Therefore, we cannot create a process for each number because it leads to excessive memory allocation and process overhead, making it impractical. Consequently, we remove the execution of `multiprocessing_loop.py` from `main.py`.
- Redo the test with 10<sup>7</sup> numbers.
- Test both synchronous and asynchronous versions in the pool.
- What are your conclusions?
    - ![The program run for squaring numbers using pooling and process pool executor](squareprogram_run.png)
    - From the results, we can see that:
        - **Sequential execution** is the most efficient for small inputs and simple programs like squaring 10<sup>6</sup> and 10<sup>7</sup> numbers.
        - **Multiprocessing Pool Synchronous version** using `map()` is more efficient compared to `apply()` since `apply()` creates a new process per call, which introduces significant overhead and slows down the execution.
        - **Multiprocessing Pool Asynchronous version** using `map_async()` performs slightly worse than `map()` since it introduces some overhead associated with managing asynchronous calls.
        - **Multiprocessing Pool Asynchronous version** using `apply_async()` performs better than `apply()` because it allows for non-blocking execution (meaning it does not prevent the execution of a task while waiting for a result), enabling other tasks to proceed while waiting for the result, thus improving overall efficiency.
        - **Multiprocessing Pooling using both synchronous and asynchronous methods** shows that `apply_async()` is more efficient in scenarios where non-blocking behavior is beneficial, as it reduces idle time and makes better use of system resources.
        - **Multiprocessing execution using `concurrent.futures.ProcessPoolExecutor`** is the most efficient among the tested methods. This is because `ProcessPoolExecutor` provides a high-level interface for asynchronously executing callables, managing a pool of processes, and efficiently distributing tasks among them, leading to improved performance.
        - **On a side note, chunking improved both pooling and process pool executor performance in terms of time** since it reduces the frequency of communicaton between processes by grouping tasks together, leading to fewer process management operation for pooling and it allows for better scheduling of tasks across worker, especially in asynchronous execution reducing the overall overhead calls for managing individual tasks for process pool executor.

---

## Process Synchronization with Semaphores
### Overview
In order to experiment on how to use semaphores in Python’s multiprocessing 
module to manage access to a limited pool of resources. Implement a ConnectionPool class that simulates a pool of database connections, using a semaphore to control access. 
- Create a ConnectionPool class with methods to get and release connections, 
using a semaphore to limit access. 
- Write a function that simulates a process performing a database operation by 
acquiring and releasing a connection from the pool. 
- Observe how the semaphore ensures that only a limited number of processes 
can access the pool at any given time.
### Instructions
----
1. Create the ConnectionPool Class
2. Implement the Database Operation Function
3. Set Up Multiprocessing
----
4. Discuss Observations
- What happens if more processes try to access the pool than there are available 
connections? 
- How does the semaphore prevent race conditions and ensure safe access to the 
connections?
---