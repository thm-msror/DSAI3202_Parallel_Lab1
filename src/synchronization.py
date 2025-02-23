import threading

data_lock = threading.RLock()
condition = threading.Condition(data_lock)