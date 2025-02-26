import time
import threading
from src.display import initialize_display, update_display
from src.thread_version import start_threads, condition

if __name__ == "__main__":
    # Start all sensor and processing threads
    start_threads()

    # Initialize and update the display
    initialize_display()

    display_thread = threading.Thread(target=update_display, args=(condition,), daemon=True)
    display_thread.start()

    # Keep main program running
    while True:
        time.sleep(1)