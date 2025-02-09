import random

# Function to add a thousand random numbers
def sum_numbers(n):
    """Calculate the sum of numbers from 1 to n."""
    total = 0
    for i in range(1, n+1):
        total += i
    return total

def threaded_sum(start, end, result_list, index):
    """Calculate sum for a portion of the range and store it in result_list."""
    total = 0
    for i in range(start, end + 1): 
        total += i
    result_list[index] = total  # Store the computed sum in the shared list
    return total
    
def process_sum(start, end, result_queue):
    """Calculate sum for a portion of the range and store it in a queue."""
    total = 0
    for i in range(start, end + 1):
        total += i
    result_queue.put(total)  # Store result in queue instead of using sum()