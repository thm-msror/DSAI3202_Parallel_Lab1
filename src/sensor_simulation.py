import random
import time

latest_temperatures = {}  # Shared dictionary for latest temperature readings

def simulate_sensor(sensor_id, temp_queue, lock):
    """Simulates temperature readings and adds them to the queue."""
    global latest_temperatures
    while True:
        temperature = random.randint(15, 40)
        
        with lock:
            latest_temperatures[sensor_id] = temperature  # Update latest readings
        
        temp_queue.put(temperature)  # Send reading to queue for processing
        time.sleep(1)
