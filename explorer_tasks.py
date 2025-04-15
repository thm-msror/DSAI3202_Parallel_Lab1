# src/explorer_tasks.py

"""
explorer_tasks.py

Defines Celery tasks for running different maze-solving algorithms in parallel.
Uses RabbitMQ as the broker and Redis as the result backend.

Tasks:
- explore_original: the wall-following (right-hand rule) explorer
- explore_bfs:      the BFS (shortest-path) explorer
- explore_astar:    the A* (heuristic) explorer

Each task returns a dict with identical keys so they can be compared:
    {
      'maze_type':     str,    # algorithm name
      'time_taken':    float,  # seconds
      'moves':         int,    # path length
      'backtracks':    int,    # number of backtracks (0 for BFS/A*)
      'moves_per_sec': float,  # moves / time_taken
    }
"""

from celery import Celery
from src.maze import create_maze
from src.explorer import Explorer           # original wall‑follower
from src.explorer_bfs import BFSExplorer    # BFS shortest‑path
from src.explorer_aStar import AStarExplorer# A* heuristic
import time

# Configure Celery: RabbitMQ broker + Redis result backend
app = Celery(
    'explorer_tasks',
    broker='pyamqp://guest@localhost//',    # RabbitMQ
    backend='redis://localhost:6379/0'      # Redis
)

@app.task
def explore_original(maze_type: str, w: int = 30, h: int = 30) -> dict:
    """
    Run the original wall‑following Explorer (right‑hand rule).

    Args:
        maze_type: 'random' or 'static'
        w, h: maze dimensions (ignored for static)

    Returns:
        stats dict
    """
    # 1. Generate maze
    maze = create_maze(w, h, maze_type)
    # 2. Create and run explorer headless
    ex = Explorer(maze, visualize=False)
    time_taken, path = ex.solve()
    # 3. Build stats
    return {
        'maze_type':     'original',
        'time_taken':    time_taken,
        'moves':         len(path),
        'backtracks':    ex.backtrack_count,
        'moves_per_sec': len(path) / time_taken if time_taken > 0 else 0
    }

@app.task
def explore_bfs(maze_type: str, w: int = 30, h: int = 30) -> dict:
    """
    Run the BFSExplorer to find the true shortest path.

    Args:
        maze_type: 'random' or 'static'
        w, h: maze dimensions (ignored for static)

    Returns:
        stats dict from BFSExplorer.solve()
    """
    maze = create_maze(w, h, maze_type)
    ex = BFSExplorer(maze)
    return ex.solve()

@app.task
def explore_astar(maze_type: str, w: int = 30, h: int = 30) -> dict:
    """
    Run the AStarExplorer with a Manhattan distance heuristic.

    Args:
        maze_type: 'random' or 'static'
        w, h: maze dimensions (ignored for static)

    Returns:
        stats dict from AStarExplorer.solve()
    """
    maze = create_maze(w, h, maze_type)
    ex = AStarExplorer(maze)
    return ex.solve()
