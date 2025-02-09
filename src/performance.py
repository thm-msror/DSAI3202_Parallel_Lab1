def compute_speedup(serial_time, parallel_time):
    return serial_time / parallel_time

def compute_efficiency(speedup, np):
    return speedup / np

def amdahls_law(np, P):
    return 1 / (((1 - P)) + (P / np))

def gustafsons_law(np, P):
    return np + (1-P)*(1-np)