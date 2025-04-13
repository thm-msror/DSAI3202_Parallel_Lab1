"""
dispatch_explorers.py

This script dispatches multiple parallel maze explorers using Celery.
It launches N explorers per maze type, collects their results, computes statistics,
and prints a summary including the best run.
"""

from explorer_tasks import explore_task  # Celery task
from collections import defaultdict      # for grouping results

def main():
    # 1. Set number of explorers per maze type
    N = 4
    maze_types = ['static']

    # 2. Launch all Celery tasks asynchronously
    async_results = []
    for mtype in maze_types:
        for i in range(N):
            async_results.append(explore_task.delay(mtype))  # fire off task to worker queue

    # 3. Wait for all tasks to complete and collect results
    results = [r.get() for r in async_results]  # blocks until task is complete

    # 4. Group results by maze type
    grouped = defaultdict(list)
    for r in results:
        grouped[r['maze_type']].append(r)
        
    # 5. Print individual explorer run results ===
    print("\n=== Individual Explorer Runs ===")
    for mtype, runs in grouped.items():
        for i, r in enumerate(runs, 1):
            print(f"[{mtype.capitalize()}] Explorer {i}: Time: {r['time_taken']:.5f}s, "
                  f"Moves: {r['moves']}, Backtracks: {r['backtracks']}, "
                  f"Moves/sec: {r['moves_per_sec']:.5f}")

    # 6. Print summary statistics
    print("\n=== Summary Statistics ===")
    for mtype, runs in grouped.items():
        avg_time   = sum(r['time_taken']    for r in runs) / len(runs)
        avg_moves  = sum(r['moves']         for r in runs) / len(runs)
        avg_back   = sum(r['backtracks']    for r in runs) / len(runs)
        avg_mps    = sum(r['moves_per_sec'] for r in runs) / len(runs)

        print(f"\nMaze Type: {mtype}")
        print(f"  Explorer (s):     {len(runs)}")
        print(f"  Avg time (s):     {avg_time:.5f}")
        print(f"  Avg moves:        {avg_moves:.5f}")
        print(f"  Avg backtracks:   {avg_back:.1f}")
        print(f"  Avg moves/sec:    {avg_mps:.5f}")

    # 7. Find and display the best single run (lowest moves)
    best = min(results, key=lambda r: r['moves'])
    print("\n=== Best Single Run ===")
    print(f"Type: {best['maze_type']}, Moves: {best['moves']}, Time: {best['time_taken']:.5f}s, Backtracks: {best['backtracks']}")

if __name__ == "__main__":
    main()
