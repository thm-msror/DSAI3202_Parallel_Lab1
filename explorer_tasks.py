# tasks.py
from celery import Celery
import time

from src.maze import create_maze
from src.explorer import Explorer

# 1. Configure Celery to use RabbitMQ as broker, and RPC as result backend
app = Celery(
    'explorer_tasks',
    broker='pyamqp://guest@localhost//',
    backend='redis://localhost:6379/0'
)

@app.task
def explore_task(maze_type: str, width: int = 30, height: int = 30) -> dict:
    """
    Run one headless Explorer on a maze of the given type and size.
    Returns a dict of statistics.
    """
    # 2. Create the maze and explorer
    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, visualize=False)

    # 3. Solve & time it
    start = time.time()
    time_taken, moves = explorer.solve()
    end = time.time()

    # 4. Collect stats
    return {
        'maze_type':      maze_type,
        'time_taken':     time_taken,
        'moves':          len(moves),
        'backtracks':     explorer.backtrack_count,
        'moves_per_sec':  len(moves) / time_taken
    }
