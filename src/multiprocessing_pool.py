import time
import multiprocessing
from src.compute_square import square

def chunk_data(data, num_chunks):
    """Splits data into roughly equal chunks."""
    chunk_size = len(data) // num_chunks
    chunks = []
    
    for i in range(num_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        chunks.append(data[start:end])

    # Add remaining elements to the last chunk if needed
    if len(data) % num_chunks:
        chunks.append(data[num_chunks * chunk_size:])

    return chunks

def process_chunk(chunk):
    """Worker function to compute squares for a chunk of numbers."""
    results = []
    for n in chunk:
        results.append(square(n))
    return results

def multiprocessing_pool_map(numbers):
    """Executes using multiprocessing pool with map() and map_async()."""
    num_chunks = multiprocessing.cpu_count()
    chunks = chunk_data(numbers, num_chunks)

    # Using map()
    start_time = time.time()
    with multiprocessing.Pool(processes=num_chunks) as pool:
        results = pool.map(process_chunk, chunks)
    end_time = time.time()

    # Using map_async()
    start_time1 = time.time()
    with multiprocessing.Pool(processes=num_chunks) as pool:
        async_result = pool.map_async(process_chunk, chunks)
        results_async = async_result.get()
    end_time1 = time.time()

    return end_time - start_time, end_time1 - start_time1

def multiprocessing_pool_apply(numbers):
    """Executes using multiprocessing pool with apply() and apply_async()."""
    num_chunks = multiprocessing.cpu_count()
    chunks = chunk_data(numbers, num_chunks)

    # Using apply()
    start_time = time.time()
    results = []
    with multiprocessing.Pool(processes=num_chunks) as pool:
        for chunk in chunks:
            result = pool.apply(process_chunk, args=(chunk,))
            results.append(result)
    end_time = time.time()

    # Using apply_async()
    start_time1 = time.time()
    results_async = []
    with multiprocessing.Pool(processes=num_chunks) as pool:
        async_results = []
        for chunk in chunks:
            async_result = pool.apply_async(process_chunk, args=(chunk,))
            async_results.append(async_result)
        
        for res in async_results:
            results_async.append(res.get())
    end_time1 = time.time()

    return end_time - start_time, end_time1 - start_time1