# dispatch_explorers.py

"""
dispatch_explorers.py

Dispatches multiple maze-solving tasks in parallel via Celery,
then collects, groups, and compares their performance statistics.
"""

from explorer_tasks import explore_original, explore_bfs, explore_astar
from collections import defaultdict

def main():
    # Number of runs per algorithm
    N = 4
    maze_type = 'static'

    # 1. Fire off all tasks
    tasks = []
    for _ in range(N):
        tasks.append(explore_original.delay(maze_type))
        tasks.append(explore_bfs.delay(maze_type))
        tasks.append(explore_astar.delay(maze_type))

    # 2. Collect results (blocks until each finishes)
    results = [t.get() for t in tasks]

    # === Print individual explorer run metrics ===
    print("\n=== Individual Explorer Runs ===")
    for idx, r in enumerate(results, start=1):
        print(f"\nRun {idx} ({r['maze_type']}): "
              f"Time: {r['time_taken']:.6f}s, "
              f"Moves: {r['moves']}, "
              f"Backtracks: {r['backtracks']}, "
              f"Moves/sec: {r['moves_per_sec']:.1f}")

    # 3. Group by algorithm name
    grouped = defaultdict(list)
    for r in results:
        grouped[r['maze_type']].append(r)

    # 4. Print aggregated summary
    print(f"\n=== Performance on '{maze_type}' Maze ===")
    for algo, runs in grouped.items():
        # Compute averages
        avg_t   = sum(r['time_taken']    for r in runs) / len(runs)
        avg_m   = sum(r['moves']         for r in runs) / len(runs)
        avg_b   = sum(r['backtracks']    for r in runs) / len(runs)
        avg_mps = sum(r['moves_per_sec'] for r in runs) / len(runs)

        print(f"\nAlgorithm: {algo}")
        print(f"  Runs:             {len(runs)}")
        print(f"  Avg time (s):     {avg_t:.6f}")
        print(f"  Avg moves:        {avg_m:.1f}")
        print(f"  Avg backtracks:   {avg_b:.1f}")
        print(f"  Avg moves/sec:    {avg_mps:.1f}")

    # 5. Identify and print the single best run (fewest moves)
    best = min(results, key=lambda r: r['moves'])
    print("\n=== Best Single Run ===")
    print(f"Algorithm: {best['maze_type']}")
    print(f"  Moves:          {best['moves']}")
    print(f"  Time:           {best['time_taken']:.6f}s")
    print(f"  Backtracks:     {best['backtracks']}")
    print(f"  Moves/sec:      {best['moves_per_sec']:.1f}")

if __name__ == "__main__":
    main()
