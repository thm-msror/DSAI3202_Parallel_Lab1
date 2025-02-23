import time
from queue import Queue

temperature_averages = {}

def process_temperatures(sensor_id, temp_queue, lock):
    """Continuously calculates average temperature from readings in the queue."""
    global temperature_averages
    readings = []
    
    while True:
        temperature = temp_queue.get()
        readings.append(temperature)
        avg_temp = sum(readings) / len(readings)

        with lock:
            temperature_averages[sensor_id] = avg_temp
        time.sleep(5)