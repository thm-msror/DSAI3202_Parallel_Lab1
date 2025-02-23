import time
from src.sensor_simulation import latest_temperatures
from src.data_processing import temperature_averages

def initialize_display():
    """Initializes the console display layout."""
    print("Current temperatures:")
    
    for sensor in range(3):
        temp = latest_temperatures.get(sensor, "--")
        print(f"Latest Temperature: Sensor {sensor}: {temp}°C")
    
    for sensor in range(3):
        avg_temp = temperature_averages.get(sensor, "--")
        print(f"Sensor {sensor} Average: {avg_temp}°C")

def update_display():
    """Continuously updates temperature readings and averages."""
    while True:
        print("\nCurrent temperatures:")
        
        for sensor, temp in latest_temperatures.items():
            print(f"Sensor {sensor}: {temp}°C", end=" ")
        print("\n")
        
        for sensor, avg in temperature_averages.items():
            print(f"Sensor {sensor} Average: {avg:.2f}°C")
        
        time.sleep(5)
