# DSAI3202 - Parallel and Distributed Computing
---
# Assignment 2 - Maze Explorer Game

A simple maze exploration game built with Pygame where you can either manually navigate through a maze or watch an automated solver find its way to the exit.

---
### Question 1 (10 points)
Explain how the automated maze explorer works. Your answer should include:
1. The algorithm used by the explorer
2. How it handles getting stuck in loops
3. The backtracking strategy it employs
4. The statistics it provides at the end of exploration

To answer this question:
1. Run the explorer both with and without visualization
2. Observe its behavior in different maze types
3. Analyze the statistics it provides
4. Read the source code in `explorer.py` to understand the implementation details

Your answer should demonstrate a clear understanding of:
- The right-hand rule algorithm
- The loop detection mechanism
- The backtracking strategy
- The performance metrics collected

### Answer 1 (10 points)
The explorer implements the right‑hand rule (also called wall‑following). At each step it:
- Turns right and checks if it can move forward.
- If blocked, goes straight.
- If still blocked, turns left.
- As a last resort, turns around (180°) and moves.

By always “keeping its right hand on the wall,” it will eventually traverse every corridor in a simply‑connected maze and reach the exit.

In the code, explorer.py, the `solve()` method implements the right‑hand rule by repeatedly calling `turn_right()`, testing `can_move_forward()`, then falling back to straight, left, or a 180° turn if necessary. 
To detect loops it keeps the last three positions in `self.move_history` and `is_stuck()` returns true when they’re identical. 
In that case it calls `backtrack()`, which builds a short path back to the last junction (using `find_backtrack_path()` and `count_available_choices()`), pops positions off `self.backtrack_path`, and moves there before resuming the wall‑following logic. Throughout, it records every move in `self.moves`, timestamps `self.start_time/self.end_time`, and increments `self.backtrack_count`. 
At the end it calls `print_statistics()`, which reports total time, total moves, number of backtracks, and average moves per second. 
If visualize=True, each move also triggers `draw_state()`, which renders the maze and explorer via Pygame (and in the Jupyter demo via visualize_maze or JupyterExplorer), whereas with visualize=False it runs headless and simply returns the raw metrics.

In `maze_visualization.py`, the demo shows performance analysis of the automated explorer on different maze types with and without visulization, without visulization it returns the raw metrics therefore the `total_time_taken` is `0.0 seconds` and with visulization it returns `total_time_taken` greater than 0.0 seconds due to the rendering overhead.
The performance metrics collected and displayed after an explorer has solved one maze are:
1. Total time taken: Shows how long the explorer takes to solve the maze, wall-clock duration from start_time = time.time to end_time = time.time.
2. Total moves made: The length of self.moves—i.e. every single step the explorer actually took in the maze. This tells you how long the path was.
3. Number of backtrack operations: The value of self.backtrack_count, incremented each time backtrack() successfully moves the explorer back to a junction. A high count indicates many dead‑ends or loops were encountered.
4. Average moves per second: Computed as len(self.moves) / time_taken. This combines path length and speed into one efficiency metric: higher means the solver covered more ground faster (or did less rendering).

Together, these four give you a complete picture of how long the solver ran, how far it traveled, how often sit got stuck and had to reverse, and how efficiently it moved through the maze.
---

### Question 2 (30 points)
Modify the main program to run multiple maze explorers simultaneously. This is because we want to find the best route out of the maze. Your solution should:
1. Allow running multiple explorers in parallel
2. Collect and compare statistics from all explorers
3. Display a summary of results showing which explorer performed best

*Hints*:
- To get 20 points, use use multiprocessing.
- To get 30 points, use MPI4Py on multiple machines.
- Use Celery and RabbitMQ to distribute the exploration tasks. You will get full marks plus a bonus.
- Implement a task queue system
- Do not visualize the exploration, just run it in parallel
- Store results for comparison

**To answer this question:** 
1. Study the current explorer implementation
2. Design a parallel execution system
3. Implement task distribution
4. Create a results comparison system
---

### Question 3 (10 points)
Analyze and compare the performance of different maze explorers on the static maze. Your analysis should:

1. Run multiple explorers (at least 4 ) simultaneously on the static maze
2. Collect and compare the following metrics for each explorer:
   - Total time taken to solve the maze
   - Number of moves made
   - *Optional*:
     - Number of backtrack operations

3. What do you notice regarding the performance of the explorers? Explain the results and the observations you made.
---

### Question 4 (20 points)
Based on your analysis from Question 3, propose and implement enhancements to the maze explorer to overcome its limitations. Your solution should:

1. Identify and explain the main limitations of the current explorer:

2. Propose specific improvements to the exploration algorithm:

3. Implement at least two of the proposed improvements:

Your answer should include:
1. A detailed explanation of the identified limitations
2. Documentation of your proposed improvements
3. The modified code with clear comments explaining the changes
---

### Question 5 (20 points)

Compare the performance of your enhanced explorer with the original:
   - Run both versions on the static maze
   - Collect and compare all relevant metrics
   - Create visualizations showing the improvements
   - Document the trade-offs of your enhancements
Your answer should include:
1. Performance comparison results and analysis
2. Discussion of any trade-offs or new limitations introduced
---

### Final points 6 (10 points)
1. Solve the static maze in 150 moves or less to get 10 points.
2. Solve the static maze in 135 moves or less to get 15 points.
3. Solve the static maze in 130 moves or less to get 100% in your assignment.