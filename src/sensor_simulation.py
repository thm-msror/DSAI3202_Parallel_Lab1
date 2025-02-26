import random
import time
from threading import RLock

latest_temperatures = {}  # Shared dictionary for latest temperature readings
data_lock = RLock()  # Lock for synchronizing access to shared data

def simulate_sensor(sensor_id, temp_queue, condition):
    """Simulates temperature readings and adds them to the queue."""
    global latest_temperatures
    while True:
        temperature = random.randint(15, 40)
        
        with condition:
            latest_temperatures[sensor_id] = temperature  # Update latest readings
            condition.notify_all()  # Notify waiting threads
        
        temp_queue.put(temperature)  # Send reading to queue for processing
        time.sleep(1)