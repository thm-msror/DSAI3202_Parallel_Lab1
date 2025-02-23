import threading
from queue import Queue
from src.sensor_simulation import simulate_sensor, latest_temperatures
from src.data_processing import process_temperatures, temperature_averages
from src.synchronization import data_lock  # Ensure this exists

NUM_SENSORS = 3
sensor_threads = []
processing_threads = []
queues = {i: Queue() for i in range(NUM_SENSORS)}

def start_threads():
    """Starts all sensor and processing threads."""
    global sensor_threads, processing_threads

    # Start sensor threads
    for i in range(NUM_SENSORS):
        thread = threading.Thread(target=simulate_sensor, args=(i, queues[i], data_lock), daemon=True)
        sensor_threads.append(thread)
        thread.start()

    # Start processing threads
    for i in range(NUM_SENSORS):
        thread = threading.Thread(target=process_temperatures, args=(i, queues[i], data_lock), daemon=True)
        processing_threads.append(thread)
        thread.start()
