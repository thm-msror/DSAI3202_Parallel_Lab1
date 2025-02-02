from src.serialVersion import serial_main
from src.threadVersion import thread_main
from src.processVersion import process_main

serial_time = serial_main()
thread_time = thread_main()
process_time = process_main()

speedupT = serial_time / thread_time
print("\nSpeedup for (serial / thread) = ", speedupT)
speedupP = serial_time / process_time
print("Speedup for (serial / process) = ", speedupP)

effT = speedupT / 4
print("\nEffeciency for (speedup of thread / no. of threads) = ", effT)
effP = speedupP / 4
print("Effeciency for (speedup of process / no. of processes) = ", effP)

