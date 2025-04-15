from .visualization import JupyterExplorer
from collections import deque
import time

class JupyterBFSExplorer(JupyterExplorer):
    def solve(self):
        start_time = time.time()
        visited = set()
        queue = deque()
        queue.append((self.maze.start_pos, []))

        while queue:
            (x, y), path = queue.popleft()
            self.x, self.y = x, y  # for visualization

            if (x, y) == self.maze.end_pos:
                time_taken = time.time() - start_time
                return time_taken, path + [(x, y)]

            if (x, y) in visited:
                continue
            visited.add((x, y))

            self.draw_state()  # 👈 Visualize current state

            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = x + dx, y + dy
                if self.maze.is_valid_move(nx, ny) and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(x, y)]))

        return None, []
