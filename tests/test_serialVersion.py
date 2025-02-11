from src.serialVersion import serial_main

def test_serial_main():
    # Test with a smaller number for faster execution during testing
    assert serial_main(100) > 0  # Ensures that the function runs and returns a positive time
    assert serial_main(1_000) > 0  
    assert serial_main(10_000) > 0  
    assert serial_main(1_000_000) > 0  
    assert serial_main(100_000_000) > 0  