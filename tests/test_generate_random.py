from src.generate_random import join_random_letters, add_random_numbers

def test_join_random_letters():
    """
    Tests if join_random_letters correctly generates a string
    of the desired length and contains only letters.
    """
    start, end = 0, 100
    result = join_random_letters(start, end)
    assert len(result) == (end - start), "The length of the generated string is incorrect"
    assert result.isalpha(), "The result should only contain alphabetic characters"

def test_add_random_numbers():
    """
    Tests if add_random_numbers correctly generates a list of numbers
    and sums them.
    """
    start, end = 0, 100
    result = add_random_numbers(start, end)
    assert isinstance(result, int), "The sum should be an integer"
    assert result > 0, "The sum should be positive since the numbers are positive"