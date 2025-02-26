import threading
from queue import Queue
from src.sensor_simulation import simulate_sensor, data_lock
from src.data_processing import process_temperatures

NUM_SENSORS = 3
sensor_threads = []
processing_threads = []
queues = {i: Queue() for i in range(NUM_SENSORS)}
condition = threading.Condition(data_lock)

def start_threads():
    """Starts all sensor and processing threads."""
    global sensor_threads, processing_threads

    # Start sensor threads
    for i in range(NUM_SENSORS):
        thread = threading.Thread(target=simulate_sensor, args=(i, queues[i], condition), daemon=True)
        sensor_threads.append(thread)
        thread.start()

    # Start processing threads
    for i in range(NUM_SENSORS):
        thread = threading.Thread(target=process_temperatures, args=(i, queues[i], condition), daemon=True)
        processing_threads.append(thread)
        thread.start()