from src.serialVersion import serial_main

def test_serial_main():
    """
    Tests if the serial version completes without errors
    and returns a positive time value.
    """
    result = serial_main(1000000)
    assert result > 0, f"Expected time to be positive, got {result}"