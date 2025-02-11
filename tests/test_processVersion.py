from src.processVersion import process_main

def test_process_main():
    # Test with a smaller range and a few processes to ensure functionality
    assert process_main(100) > 0  # Test with a smaller input
    assert process_main(1_000) > 0 
    assert process_main(10_000, num_processes=4) > 0 
    assert process_main(100_000_000, num_processes=6) > 0 