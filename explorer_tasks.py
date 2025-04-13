"""
explorer_tasks.py

This file defines a Celery task that runs a maze explorer in a headless (non-visual) mode.
It creates a maze, runs an explorer on it, collects performance statistics, and returns them.

It uses Celery + RabbitMQ as the task queue system to run multiple explorers in parallel.
"""

from celery import Celery  # Celery for parallel task execution
import time                # for timing
from src.maze import create_maze  # maze generation
from src.explorer import Explorer  # maze-solving agent

# 1. Configure Celery with RabbitMQ (broker) and Redis (result backend)
app = Celery(
    'explorer_tasks',
    broker='pyamqp://guest@localhost//',         # RabbitMQ broker
    backend='redis://localhost:6379/0'           # Redis result backend to store task outputs
)

@app.task
def explore_task(maze_type: str, width: int = 30, height: int = 30) -> dict:
    """
    Celery task to run a maze explorer on a generated maze.
    
    Args:
        maze_type (str): Type of maze to generate (e.g., 'static', 'random').
        width (int): Width of the maze.
        height (int): Height of the maze.

    Returns:
        dict: A dictionary with exploration statistics:
            - maze_type
            - time_taken
            - moves
            - backtracks
            - moves_per_sec
    """
    # 2. Create the maze and explorer (no visualization)
    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, visualize=False)

    # 3. Solve the maze and measure time
    start = time.time()
    time_taken, moves = explorer.solve()  # explorer.solve() should return actual time and moves
    end = time.time()

    # 4. Collect and return statistics
    return {
        'maze_type':      maze_type,
        'time_taken':     time_taken,
        'moves':          len(moves),
        'backtracks':     explorer.backtrack_count,  # this should be tracked inside Explorer class
        'moves_per_sec':  len(moves) / time_taken if time_taken > 0 else 0
    }
