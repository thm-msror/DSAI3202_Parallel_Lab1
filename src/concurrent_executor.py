import time
from concurrent.futures import ProcessPoolExecutor
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

def concurrent_execution(numbers):
    """Executes using concurrent.futures ProcessPoolExecutor with chunking."""
    num_chunks = min(len(numbers), 6)  # Use number of available CPUs
    chunks = chunk_data(numbers, num_chunks)

    # Using map() with chunking
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_chunk, chunks))
    end_time = time.time()

    return end_time - start_time