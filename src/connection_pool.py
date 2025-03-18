from multiprocessing import Semaphore

class ConnectionPool:
    def __init__(self, size):
        """
        Initialize the connection pool with a fixed number of connections.
        :param size: Number of connections in the pool.
        """
        self.connections = list(range(size))  # Simulate connections (e.g., [0, 1, 2])
        self.semaphore = Semaphore(size)      # Semaphore to control access

    def get_connection(self):
        """
        Acquire a connection from the pool.
        """
        self.semaphore.acquire()  # Wait for a connection to be available
        connection = self.connections.pop(0)  # Remove the first connection from the pool
        print(f"Acquired connection: {connection}")
        return connection

    def release_connection(self, connection):
        """
        Release a connection back to the pool.
        :param connection: The connection to release.
        """
        self.connections.append(connection)  # Add the connection back to the pool
        print(f"Released connection: {connection}")
        self.semaphore.release()  # Signal that a connection is available