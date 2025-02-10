# DSAI 3202 – Parallel and Distributed Computing  
## Lab 3: Part 1 - Data Parallel Model
---
### Objectives
- Build a data parallel model program using threads in Python.
- Build a data parallel model program using processes in Python.
- Understand the basics of parallel programming using Python's `threading` and `multiprocessing` modules.
---
## Q. Divide the range of numbers (1 to n) into multiple equal parts and assign each part to a separate thread (Hint: make sure to make a copy of each part). 
---
### A generalized instruction on how to split n into chunks:
#### Steps to Divide the Range into Chunks, Assign Each to a Separate Thread or Process, and Collect the Results.

#### 1. Calculate Chunk Size
```python
chunk_size = n // num_threads  # For threading
```

### 2. Divide the Range into Chunks
Now, divide the range from 1 to n into equal chunks. 
The range will be split based on the number of threads or processes. 
Each thread or process will be assigned a chunk of numbers.
```python
for i in range(num_threads):  
    start = i * chunk_size + 1
    end = (i + 1) * chunk_size
    if i == num_threads - 1:  
        end = n
```

### 3. Assign Each Chunk to a Separate Thread or Process
Create a thread or process for each chunk and assign it the range of numbers.
```python
for i in range(num_threads):  # For threading
    thread = threading.Thread(target=thread_worker, args=(start, end))
    threads.append(thread)
    print(f"Created thread for range {start} to {end}")
    thread.start()
```
where thread_worker or process_worker function processes a specific chunk of data assigned to it, performing the designated task on that portion
```python
# Worker function inside thread_main
    def thread_worker(start, end):
        partial_sum = compute_sum(start, end)
        result_queue.put(partial_sum) 
```
This version creates a local copy of the range (from start to end) in local_range, and then manually sums the numbers within that range. After computing the sum, the result is added to the result_queue.
```python
# Worker function inside thread_main
def thread_worker(start, end):
    # Create a local copy of the range (if needed)
    local_range = range(start, end + 1)  # This creates a new range object for the thread
    partial_sum = 0
    for number in local_range:
        partial_sum += number  # Sum up the numbers in the local range
    result_queue.put(partial_sum)
```
The second version (using local_range) can be useful if you need to work with the chunk in isolation (for example, if you want to modify the data without affecting other threads or processes). However, in the current context, if the compute_sum function handles summing the range correctly, the first version would be more efficient as it doesn't need the extra step of creating a range object and copying the data.

### 4. Handle the Last Thread or Process
The last thread or process may have more numbers to sum if n is not perfectly divisible by the number of threads or processes. Ensure that the last chunk includes any remaining numbers.
```python
if i == num_threads - 1:  # Ensure the last thread covers remaining numbers
    end = n
```

### 5. Collect Results from Threads or Processes
After all threads or processes have completed their tasks, collect the partial sums from each thread or process.
```python
# Collect results from queue
total_sum = 0
while not result_queue.empty():
    partial_sum = result_queue.get()
    total_sum += partial_sum
```
---
### How does the execution time change when moving from sequential to threaded to multiprocessing implementations?

The execution time typically changes as follows when moving from sequential to threaded to multiprocessing implementations:
- **Sequential:** Baseline execution time.
- **Threaded:** Often slower or similar to sequential due to Global Interpreter Lock (GIL) limitations.
- **Multiprocessing:** Significantly faster for CPU-bound tasks, potentially cutting execution time by half or more.

### Are there any performance differences between the threaded and multiprocessing versions?

1.  **Regarding the difference between queue.Queue() and multiprocessing.Queue():**
- queue.Queue() is used for thread-safe communication within a single process.
  - It's suitable for multithreading scenarios wherthreads share the same memory space.
- multiprocessing.Queue() is designed for inter-process communication.
  - It allows safe data exchange between separate processes, each with its own memory space.
 
2. **Threading:** There is a small speedup, but the performance gain is limited due to Python's GIL, which prevents true parallel execution.
   
3. **Multiprocessing:** This approach offers the best speedup and efficiency, especially for CPU-bound tasks, as it bypasses the GIL and can fully utilize multiple cores.

### What challenges did you face when implementing parallelism, and how did you address them?
1. **Threading performance:** Initially, threading was not providing a significant performance improvement over the serial approach. To address this, I increased the number of threads and the input size n to better visualize the impact of threading. This was particularly useful when the workload could be distributed across multiple threads.

2. **Thread safety:** I switched from using lists to queues for communication between threads. This change ensured thread safety and avoided potential race conditions while sharing data between threads.

3. **Multiprocessing:** In multiprocessing, I faced issues with data sharing, especially when passing large data between processes. To avoid issues like pickling, I kept the process_worker function in the same function as process_main to prevent serialization of objects and ensure smooth data handling.

### When would you choose threading over multiprocessing or vice versa for parallel tasks?

1. **Threading:** In Python, threads share the same memory space, and the GIL (Global Interpreter Lock) restricts the ability of threads to truly run in parallel on multiple CPU cores for CPU-bound operations. While threading can still help with I/O-bound tasks, it's limited for CPU-bound work.
   
2. **Multiprocessing:** Each process in multiprocessing runs in its own memory space, which bypasses the GIL and allows full parallelism on multiple CPU cores.

---
