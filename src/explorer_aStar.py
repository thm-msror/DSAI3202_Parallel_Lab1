# src/explorer_aStar.py

import time
import heapq

class AStarExplorer:
    """A* search explorer with Manhattan‐distance heuristic for optimal, guided search."""

    def __init__(self, maze):
        self.maze  = maze
        self.start = maze.start_pos
        self.end   = maze.end_pos

    def solve(self):
        # Record start time with high resolution
        start_time = time.perf_counter()

        # open_set holds (f_score, g_score, position, path)
        # f_score = g_score + heuristic
        open_set = [(self._h(self.start), 0, self.start, [self.start])]
        g_score  = {self.start: 0}
        visited  = set()

        # Unlike wall‑following, A* uses both actual cost (g) and heuristic (h)
        # to pick the most promising node first.
        while open_set:
            f, g, pos, path = heapq.heappop(open_set)
            if pos in visited:
                continue
            visited.add(pos)

            # Terminate as soon as we pop the goal: guaranteed optimal path
            if pos == self.end:
                end_time = time.perf_counter()
                return self._stats(path, start_time, end_time)

            x, y = pos
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nxt = (x + dx, y + dy)
                # Standard grid neighbor check
                if (0 <= nxt[0] < self.maze.width and
                    0 <= nxt[1] < self.maze.height and
                    self.maze.grid[nxt[1]][nxt[0]] == 0):
                    tentative_g = g + 1
                    # Only consider this neighbor if we've found a cheaper path
                    if tentative_g < g_score.get(nxt, float('inf')):
                        g_score[nxt] = tentative_g
                        f_score      = tentative_g + self._h(nxt)
                        heapq.heappush(open_set,
                                       (f_score, tentative_g, nxt, path + [nxt]))

        raise RuntimeError("No path found")

    def _h(self, pos):
        # Manhattan distance: admissible heuristic for 4‑way grids
        return abs(pos[0] - self.end[0]) + abs(pos[1] - self.end[1])

    def _stats(self, path, start, end):
        """
        Convert the path into stats, same as BFSExplorer:
        - steps = len(path) - 1
        - A* also never backtracks in the sense of undoing steps.
        """
        time_taken = end - start
        steps      = max(0, len(path) - 1)
        return {
            'maze_type':     'optimized_astar',
            'time_taken':    time_taken,
            'moves':         steps,
            'backtracks':    0,
            'moves_per_sec': steps / time_taken if time_taken > 0 else 0
        }
