def compute_speedup(serial_time, parallel_time):
    return serial_time / parallel_time

def compute_efficiency(speedup, num_units):
    return speedup / num_units

def amdahls_law(S, P):
    return 1 / ((1 - P) + (P / S))

def gustafsons_law(S, P):
    return P + S * (1 - P)
