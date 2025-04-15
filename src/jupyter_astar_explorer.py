from .visualization import JupyterExplorer
import heapq
import time

class JupyterAStarExplorer(JupyterExplorer):
    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve(self):
        start_time = time.time()
        start = self.maze.start_pos
        end = self.maze.end_pos

        open_set = []
        heapq.heappush(open_set, (0 + self.heuristic(start, end), 0, start, []))
        visited = set()

        while open_set:
            f, g, current, path = heapq.heappop(open_set)
            x, y = current
            self.x, self.y = x, y  # for visualization

            if current == end:
                time_taken = time.time() - start_time
                return time_taken, path + [current]

            if current in visited:
                continue
            visited.add(current)

            self.draw_state()  # 👈 Visualize current state

            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = x + dx, y + dy
                neighbor = (nx, ny)
                if self.maze.is_valid_move(nx, ny) and neighbor not in visited:
                    heapq.heappush(open_set, (
                        g + 1 + self.heuristic(neighbor, end),
                        g + 1,
                        neighbor,
                        path + [current]
                    ))

        return None, []