from src.sum_num import compute_sum

def test_compute_sum():
    assert compute_sum(1, 10) == 55
    assert compute_sum(1, 5) == 15
    assert compute_sum(10, 20) == 165
    assert compute_sum(100, 100) == 100
    assert compute_sum(0, 0) == 0