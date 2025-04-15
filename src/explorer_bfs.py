# src/explorer_bfs.py

import time
from collections import deque

class BFSExplorer:
    """Breadth‑First Search explorer: guarantees the shortest path."""

    def __init__(self, maze):
        self.maze  = maze
        self.start = maze.start_pos
        self.end   = maze.end_pos

    def solve(self):
        # Record high‑precision start time
        start_time = time.perf_counter()

        # BFS uses a queue of (position, path_so_far)
        queue   = deque([(self.start, [self.start])])
        visited = {self.start}  # Prevents revisiting cells

        # Unlike right‑hand rule, which only looks at one direction at a time
        # and may loop, BFS explores all neighbors level by level.
        while queue:
            pos, path = queue.popleft()

            # If we've reached the goal, stop immediately: this is the shortest path.
            if pos == self.end:
                end_time = time.perf_counter()
                return self._stats(path, start_time, end_time)

            x, y = pos
            # Explore all 4 directions uniformly, instead of preferring right‑turns
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nxt = (x + dx, y + dy)
                # Check bounds, walls, and unvisited
                if (0 <= nxt[0] < self.maze.width and
                    0 <= nxt[1] < self.maze.height and
                    self.maze.grid[nxt[1]][nxt[0]] == 0 and
                    nxt not in visited):
                    visited.add(nxt)
                    queue.append((nxt, path + [nxt]))

        # If the maze is valid, we should never get here
        raise RuntimeError("No path found")

    def _stats(self, path, start, end):
        """
        Convert the path (list of nodes) into statistics.
        - steps = len(path) - 1 because path includes the start node.
        - BFS has no backtracking in the sense of undoing steps.
        """
        time_taken = end - start
        steps      = max(0, len(path) - 1)
        return {
            'maze_type':     'optimized_bfs',
            'time_taken':    time_taken,
            'moves':         steps,
            'backtracks':    0,
            'moves_per_sec': steps / time_taken if time_taken > 0 else 0
        }
