import pytest
from src.performance import compute_speedup, compute_efficiency, amdahls_law, gustafsons_law

def test_compute_speedup():
    """
    Tests if the speedup is calculated correctly.
    """
    serial_time = 10
    parallel_time = 5
    result = compute_speedup(serial_time, parallel_time)
    assert result == 2, f"Expected 2, got {result}"

def test_compute_efficiency():
    """
    Tests if efficiency is calculated correctly.
    """
    speedup = 2
    num_units = 4
    result = compute_efficiency(speedup, num_units)
    assert result == 0.5, f"Expected 0.5, got {result}"

def test_amdahls_law():
    """
    Tests if Amdahl's Law is calculated correctly.
    """
    S, P = 10, 0.8
    result = amdahls_law(S, P)
    expected = 1 / ((1 - P) + (P / S))
    assert result == pytest.approx(expected, rel=1e-9), f"Expected {expected}, got {result}"


def test_gustafsons_law():
    """
    Tests if Gustafson's Law is calculated correctly.
    """
    S, P = 10, 0.8
    result = gustafsons_law(S, P)
    assert result == 0.8 + 10 * (1 - 0.8), f"Expected {0.8 + 10 * (1 - 0.8)}, got {result}"