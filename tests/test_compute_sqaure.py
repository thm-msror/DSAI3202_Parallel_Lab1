from src.compute_square import square

def test_square():
    assert square(2) == 4
    assert square(0) == 0
    assert square(-3) == 9