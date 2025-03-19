# DSAI 3202 – Parallel and Distributed Computing  
## Lecture 6 - Distributed Computing with Python - celery, rabbitMQ and docker tutorial

---

### Tutorial on celery

- This tutorial demonstrates how to use **Celery** with **RabbitMQ** for distributed task processing in Python. 
- The example computes the squares of numbers from 1 to 10,000 using Celery workers.

- **To run the main.py file**:
    - Run RabbitMQ on PC cmd using the command ssh -L 15672:localhost:15672 user@ip_address
    - Run  celery -A src.tasks worker --loglevel=info in VS code terminal
    - In Another VS code terminal run python main.py

---