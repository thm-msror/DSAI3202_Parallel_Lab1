from multiprocessing import Semaphore, Lock, Manager

class ConnectionPool:
    def __init__(self, size):
        """
        Initialize the connection pool with a fixed number of connections.
        :param size: Number of connections in the pool.
        """
        self.manager = Manager()
        self.connections = self.manager.list(range(size))  # Shared list of connections
        self.semaphore = Semaphore(size)                  # Semaphore to control access
        self.lock = Lock()                                # Lock for thread-safe access

    def get_connection(self):
        """
        Acquire a connection from the pool.
        """
        self.semaphore.acquire()  # Wait for a connection to be available
        with self.lock:           # Ensure thread-safe access to the connection list
            connection = self.connections.pop(0)  # Remove the first connection
        print(f"Acquired connection: {connection}")
        return connection

    def release_connection(self, connection):
        """
        Release a connection back to the pool.
        :param connection: The connection to release.
        """
        with self.lock:  # Ensure thread-safe access to the connection list
            self.connections.append(connection)  # Add the connection back to the pool
        print(f"Released connection: {connection}")
        self.semaphore.release()  # Signal that a connection is available