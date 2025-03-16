from celery import Celery

app = Celery("tasks", broker = "pyamqp://guest@localhost//") #name the file the same as the first argument

@app.task
def power(number, exponent):
    return number ** exponent