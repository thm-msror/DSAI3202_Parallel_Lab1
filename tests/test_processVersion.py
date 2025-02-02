from src.processVersion import process_main

def test_process_main():
    """
    Tests if the multiprocessing version completes without errors
    and returns a positive time value.
    """
    result = process_main(1000000)
    assert result > 0, f"Expected time to be positive, got {result}"
