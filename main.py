import time
from src.tasks import power
from src.dispatch_tasks import dispatch

if __name__ == "__main__":
    start = time.time()
    results = dispatch()
    end = time.time()
    print(f"Execution Time: {end - start:.4f} seconds")
    print(results[:10])
    
# Run RabbitMQ on PC cmd using the command ssh -L 15672:localhost:15672 user@10.102.10.67
# Run  celery -A src.tasks worker --loglevel=info in VS code terminal
# In Another terminal run python main.py