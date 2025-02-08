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
    np = 4
    result = compute_efficiency(speedup, np)
    assert result == 0.5, f"Expected 0.5, got {result}"
    
#pytest.approx ensures that the test passes if the result is close to the expected value.

def test_amdahls_law():
    """
    Tests if Amdahl's Law is calculated correctly.
    """
    np = 6  # Number of processors
    P = 0.64  # Parallel fraction
    expected_result = 1 / ((1 - P) + (P / np))  # Amdahl's Law formula
    result = amdahls_law(np, P)
    assert pytest.approx(result) == expected_result, f"Expected {expected_result}, got {result}"

def test_gustafsons_law():
    """
    Tests if Gustafson's Law is calculated correctly.
    """
    np = 6  # Number of processors
    P = 0.64  # Parallel fraction
    expected_result = np + (1 - P) * (1 - np)  # Gustafson's Law formula
    result = gustafsons_law(np, P)
    assert pytest.approx(result) == expected_result, f"Expected {expected_result}, got {result}"