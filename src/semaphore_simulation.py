from multiprocessing import Process
from src.database_operations import access_database
from src.connection_pool import ConnectionPool

def run_semaphore_simulation():
    pool = ConnectionPool(size=3)  # Create a connection pool with 3 connections
    processes = []

    # Create 10 processes
    for i in range(10):
        p = Process(target=access_database, args=(pool, i))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("All processes have completed.")