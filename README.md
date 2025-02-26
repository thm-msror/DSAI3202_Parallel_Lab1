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
  - In the parallel execution, the task of processing images is divided into chunks, and each chunk is processed by a separate process using Python's ProcessPoolExecutor.
  - This allows multiple images to be processed concurrently, utilizing multiple CPU cores, which significantly speeds up the overall execution time.
  - The images are processed in parallel by splitting the work into manageable chunks.
  - Results are accumulated in shared memory lists managed by the Manager from the multiprocessing module.
  - Progress is tracked using tqdm to monitor the status of each chunk's processing.
    
- Analyze the speedup and efficiency of the parallel execution. Discuss the results and any trade-offs encountered.
  - The parallel execution achieved a speedup of approximately 4.04, meaning it was about four times faster than the sequential execution for the same task.
  - This substantial reduction in time demonstrates the benefit of parallelization, where multiple CPU cores process images concurrently.
  - However, the efficiency, calculated as 0.67, indicates that for each process, only 67% of the CPU's potential is utilized, which suggests some overhead from process management and shared resource handling.
  - While parallelization provides a performance boost, this comes at the cost of slightly reduced efficiency and increased memory usage, as multiple processes require their own memory space and coordination.




