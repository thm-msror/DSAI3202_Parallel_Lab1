from mpi4py import MPI
import numpy as np
from src.calculate_squares import square
import time
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print(f"The process is of rank {rank}, and the size is {size}")

if rank == 0:
    #create a vector of numbers
    numbers = np.arange(size, dtype="i")
    print(numbers)
else:
    numbers = None
print(numbers)

#Create a vector of zeros
number = np.zeros(1, dtype="i")
#Scatter is broadcasting rank 0 distributes the data (numbers and number) to all other processes or machines, and one process takes one number
comm.Scatter(numbers, number, root=0)
print(numbers)
print(number)

result = square(number[0])
print(result)
time.sleep(random.randint(1, 10))
request = comm.isend(result, dest=0, tag=rank)

if rank == 0:
    results = np.zeros(size, dtype="i")
    for i in range(size):
        results[i] = comm.irecv(source=i, tag=i).wait() #create the request and wait
    print(f"The results are: {results}") 

#request.wait() #wait for all the request to be done like thread.join()