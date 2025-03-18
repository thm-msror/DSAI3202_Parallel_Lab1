from multiprocessing import Process
from src.connection_pool import ConnectionPool
from src.database_operations import access_database

def run_semaphore_simulation():
    """Runs the semaphore simulation for database connections."""
    print("\nRunning semaphore simulation for database connections...")

    # Create a connection pool with 3 connections
    pool = ConnectionPool(3)

    # Create 10 processes to simulate concurrent access
    processes = []
    for i in range(10):
        p = Process(target=access_database, args=(pool, i))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("All processes have completed.")