import time
from collections import defaultdict
from threading import RLock

temperature_averages = defaultdict(float)  # Shared dictionary for average temperatures
data_lock = RLock()  # Lock for synchronizing access to shared data

def process_temperatures(sensor_id, temp_queue, condition):
    """Processes temperature readings and calculates averages."""
    global temperature_averages
    readings = []
    
    while True:
        if not temp_queue.empty():
            temperature = temp_queue.get()
            readings.append(temperature)
            
            # Calculate average temperature
            with condition:
                temperature_averages[sensor_id] = sum(readings) / len(readings)
                condition.notify_all()  # Notify waiting threads
        
        time.sleep(1)