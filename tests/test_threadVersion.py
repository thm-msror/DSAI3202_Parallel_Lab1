from src.threadVersion import thread_main

def test_thread_main():
    # Test with a smaller range and a few threads to ensure functionality
    assert thread_main(100) > 0  # Test with a smaller input to ensure function runs correctly
    assert thread_main(1_000) > 0  
    assert thread_main(10_000, num_threads=4) > 0  
    assert thread_main(100_000_000, num_threads=6) > 0 