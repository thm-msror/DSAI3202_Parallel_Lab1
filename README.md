# DSAI 3202 – Parallel and Distributed Computing  
## Lab 4: Part 1 - Temperature Monitoring System
---
### Objectives
- Develop a Python program that simulates temperature readings from multiple sensors,
  calculates average temperatures and displays the information in real time in the console.
---
## Q1) Which synchronization metric did you use for each task? 
---
- Sensor Simulation: Condition and RLock for updating latest_temperatures and notifying threads.
- Data Processing: Condition and RLock for updating temperature_averages and notifying threads.
- Display Logic: Condition and RLock for refreshing the display without race conditions.
---
## Q2) Why did the professor not ask you to compute metrics?
---
- The lab focuses on parallelism and synchronization, not statistical analysis, to keep the learning objectives clear and straightforward.
- The lab emphasizes real-time updates and synchronization, which are more relevant to parallel and distributed computing than statistical metrics.
- Adding metrics would increase complexity without adding significant educational value.
