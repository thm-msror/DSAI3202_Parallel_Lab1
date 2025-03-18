import time
import random

def access_database(pool, process_id):
    """
    Simulate a process performing a database operation.
    :param pool: The ConnectionPool instance.
    :param process_id: The ID of the process.
    """
    print(f"Process {process_id} is waiting for a connection...")
    connection = pool.get_connection()  # Acquire a connection
    print(f"Process {process_id} has acquired connection: {connection}")
    
    # Simulate work (e.g., querying the database)
    sleep_duration = random.randint(1, 3)
    print(f"Process {process_id} is working for {sleep_duration} seconds...")
    time.sleep(sleep_duration)
    
    # Release the connection
    pool.release_connection(connection)
    print(f"Process {process_id} has released connection: {connection}")