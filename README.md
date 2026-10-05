# Heap-Data-Structures-Implementation-Analysis-and-Applications
This submission contains an in-place max-heap heapsort, an indexed max-priority queue, a single-processor task scheduler, and a reproducible sorting benchmark.

## Files

- `heapsort.py` — ascending, in-place heapsort.
- `priority_queue.py` — task records, indexed binary max-heap, and non-preemptive scheduler simulation.
- `benchmark.py` — benchmark implementations for heapsort, randomized three-way quicksort, and mergesort.
- `benchmark_results.csv` — median timings collected for the report.
- `REPORT.md` — design, complexity analysis, benchmark discussion, and scheduling example.

## Run

Use Python 3.9 or later. From this directory:

```sh
python heapsort.py
python priority_queue.py
python benchmark.py
```

The benchmark uses deterministic input generation (seed 2026), three repetitions per case, and reports the median elapsed time. Results will vary with Python version, hardware, and system load.

## Summary

Heapsort has Θ(n log n) best, average, and worst-case time and Θ(1) auxiliary space. The priority queue stores tasks in a list-backed binary max-heap and a task-ID-to-index dictionary, allowing key updates in O(log n) after O(1) lookup. The scheduler runs the highest priority task available when the processor becomes idle; it is non-preemptive and reports whether each task completed by its deadline.
