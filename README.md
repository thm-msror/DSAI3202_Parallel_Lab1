# DSAI 3202 – Parallel and Distributed Computing  
## Lab 4: Part 2 - Brain Tumor Detection Image Processing using Parallel Processing
---
### Objectives
- Develop a machine-learning model for detecting brain tumors from MRI images.
- Leverage the power of parallel processing to efficiently handle the large dataset and speed up the computation-intensive tasks involved in image processing and model training.
---
## Parallel Image Filtering
- In this part of the assignment, you will create a function for each filter and apply them in parallel to the images.
- You will store the results in dictionaries, similar to the example shown previously.
- Make sure to handle synchronization appropriately, as multiple threads or processes will access the images.

### Tasks
**Sequential execution:**
1. Loop through the images in both lists: `yes_images` and `no_images` and apply the filters in parallel.
2. For each image, create a dictionary containing the original and filtered images.
3. Store these dictionaries in two lists: `yes_inputs` for images with tumors and `no_inputs` for images without tumors.
4. Time the execution to compute the speed up and the efficiency later.
  
**Parallel execution:**
1. Create a separate function for each filter and write to be executed in parallel using either multiprocessing or multithreading.
2. Use a multiprocessing to manage parallel execution of the filter functions on the images and or the concurrent application on multiple images at the same time.
3. Implement synchronization mechanisms to ensure safe access to shared resources.
4. Measure the execution time of the parallel processing to compare it with the sequential execution.

## Analysis:
- Explain your parallelization
  - The program uses parallelization through the ProcessPoolExecutor from the concurrent.futures module to distribute image processing tasks across multiple CPU cores.
  - Each image is processed independently by a separate worker, and the work is divided into chunks to optimize resource utilization.
  - The results from each chunk are collected and merged using a shared list managed by Manager, ensuring thread-safe updates across processes.
    
- Analyze the speedup and efficiency of the parallel execution. Discuss the results and any trade-offs encountered.
  - Speedup: Parallel execution achieved a significant reduction in processing time compared to the sequential version, as tasks were distributed across multiple processors.
      - This speedup is a direct result of parallelizing independent operations (image processing) that could be performed concurrently without data dependency.
  - Efficiency: The efficiency of parallelization, measured as speedup divided by the number of processors, shows room for improvement.
      - While the processing time was reduced, the efficiency is less than ideal due to overhead introduced by managing multiple processes, task scheduling, and shared memory access.
      - If the dataset grows significantly, the efficiency may decrease further because of this overhead, leading to diminishing returns from additional parallel workers.



