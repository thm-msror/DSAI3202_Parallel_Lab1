def compute_sum(start, end):
    """Manually compute the sum for a given range."""
    total = 0
    for j in range(start, end + 1):
        total += j
    return total