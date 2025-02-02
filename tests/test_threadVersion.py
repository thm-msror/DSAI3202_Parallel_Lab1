from src.threadVersion import thread_main

def test_thread_main():
    """
    Tests if the threading version completes without errors
    and returns a positive time value.
    """
    result = thread_main(1000000)
    assert result > 0, f"Expected time to be positive, got {result}"
