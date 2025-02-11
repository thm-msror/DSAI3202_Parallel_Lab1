import pytest
from src.performance import compute_speedup, compute_efficiency, amdahls_law, gustafsons_law

def test_compute_speedup():
    assert compute_speedup(100, 20) == 5
    assert compute_speedup(10, 2) == 5
    assert compute_speedup(50, 25) == 2

def test_compute_efficiency():
    assert compute_efficiency(5, 10) == 0.5
    assert compute_efficiency(10, 5) == 2
    assert compute_efficiency(2, 4) == 0.5

def test_amdahls_law():
    assert amdahls_law(4, 0.75) == pytest.approx(2.285714, rel=1e-4)  
    assert amdahls_law(10, 0.5) == pytest.approx(1.8181818181818181, rel=1e-4)  
    assert amdahls_law(8, 0.9) == pytest.approx(4.7058823529411775, rel=1e-4)  

def test_gustafsons_law():
    assert gustafsons_law(4, 0.75) == pytest.approx(3.25, rel=1e-4)  
    assert gustafsons_law(10, 0.5) == pytest.approx(5.5, rel=1e-4)  
    assert gustafsons_law(8, 0.9) == pytest.approx(7.3, rel=1e-4)  
