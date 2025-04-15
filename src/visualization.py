"""
Visualization utilities for the maze game.
"""

import pygame
import time
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from .constants import WINDOW_SIZE, CELL_SIZE, WHITE, BLACK, RED, GREEN, BLUE
from .explorer import Explorer
import heapq
from collections import deque


def visualize_maze(maze, screen):
    """
    Visualize a maze on the given screen.
    
    Args:
        maze: The maze to visualize
        screen: The Pygame screen to draw on
    """
    # Clear the screen
    screen.fill(WHITE)
    
    # Draw maze
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x] == 1:
                pygame.draw.rect(screen, BLACK,
                               (x * CELL_SIZE, y * CELL_SIZE,
                                CELL_SIZE, CELL_SIZE))
    
    # Draw start and end points
    pygame.draw.rect(screen, GREEN,
                    (maze.start_pos[0] * CELL_SIZE,
                     maze.start_pos[1] * CELL_SIZE,
                     CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED,
                    (maze.end_pos[0] * CELL_SIZE,
                     maze.end_pos[1] * CELL_SIZE,
                     CELL_SIZE, CELL_SIZE))
    
    # Update the display
    pygame.display.flip()
    
    # Convert Pygame surface to numpy array for display
    data = pygame.surfarray.array3d(screen)
    data = np.transpose(data, (1, 0, 2))
    
    # Display the maze
    plt.figure(figsize=(10, 10))
    plt.imshow(data)
    plt.axis('off')
    plt.show()

class JupyterExplorer(Explorer):
    """
    Explorer class adapted for Jupyter notebook visualization.
    """
    def __init__(self, maze, screen):
        super().__init__(maze, visualize=True)
        self.screen = screen
        
    def draw_state(self):
        """Override draw_state to work with Jupyter"""
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Draw maze
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, BLACK,
                                   (x * CELL_SIZE, y * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE))
        
        # Draw start and end points
        pygame.draw.rect(self.screen, GREEN,
                        (self.maze.start_pos[0] * CELL_SIZE,
                         self.maze.start_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, RED,
                        (self.maze.end_pos[0] * CELL_SIZE,
                         self.maze.end_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        
        # Draw explorer
        pygame.draw.rect(self.screen, BLUE,
                        (self.x * CELL_SIZE, self.y * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        
        # Update the display
        pygame.display.flip()
        
        # Convert Pygame surface to numpy array for display
        data = pygame.surfarray.array3d(self.screen)
        data = np.transpose(data, (1, 0, 2))
        
        # Display the current state
        plt.figure(figsize=(10, 10))
        plt.imshow(data)
        plt.axis('off')
        plt.show()
        
        # Small delay to see the movement
        time.sleep(0.1)
        
        # Clear the output for the next frame
        clear_output(wait=True) 

class JupyterBFSExplorer(JupyterExplorer):
    """
    Visualize BFS pathfinding in a Jupyter notebook.
    Finds the shortest path, then animates it step by step.
    """
    def solve(self):
        start = self.maze.start_pos
        end   = self.maze.end_pos

        # 1. BFS to find the shortest path
        queue   = deque([(start, [start])])
        visited = {start}
        t0      = time.time()
        path    = []

        while queue:
            pos, p = queue.popleft()
            if pos == end:
                path = p
                break
            x, y = pos
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nxt = (x+dx, y+dy)
                if (0 <= nxt[0] < self.maze.width and
                    0 <= nxt[1] < self.maze.height and
                    self.maze.grid[nxt[1]][nxt[0]] == 0 and
                    nxt not in visited):
                    visited.add(nxt)
                    queue.append((nxt, p + [nxt]))

        t1 = time.time()
        time_taken = t1 - t0

        # 2. Animate the final path
        for x, y in path:
            self.x, self.y = x, y
            self.draw_state()

        return time_taken, path


class JupyterAStarExplorer(JupyterExplorer):
    """
    Visualize A* (Manhattan heuristic) pathfinding in a Jupyter notebook.
    Finds the shortest path, then animates it step by step.
    """
    def _h(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve(self):
        start = self.maze.start_pos
        end   = self.maze.end_pos

        # 1. A* to find the shortest path
        open_set = [(self._h(start, end), 0, start, [start])]
        g_score  = {start: 0}
        visited  = set()
        t0       = time.time()
        path     = []

        while open_set:
            f, g, pos, p = heapq.heappop(open_set)
            if pos in visited:
                continue
            visited.add(pos)

            if pos == end:
                path = p
                break

            x, y = pos
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nxt = (x+dx, y+dy)
                if (0 <= nxt[0] < self.maze.width and
                    0 <= nxt[1] < self.maze.height and
                    self.maze.grid[nxt[1]][nxt[0]] == 0):
                    tentative_g = g + 1
                    if tentative_g < g_score.get(nxt, float('inf')):
                        g_score[nxt] = tentative_g
                        heapq.heappush(open_set, (
                            tentative_g + self._h(nxt, end),
                            tentative_g,
                            nxt,
                            p + [nxt]
                        ))

        t1 = time.time()
        time_taken = t1 - t0

        # 2. Animate the final path
        for x, y in path:
            self.x, self.y = x, y
            self.draw_state()

        return time_taken, path
