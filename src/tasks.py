from celery import Celery

app = Celery(
    "tasks", 
    broker = "pyamqp://guest@localhost//", #name the python file the same as the first argument
    backend="redis://localhost:6379/0"
)

@app.task
def power(number, exponent):
    return number ** exponent