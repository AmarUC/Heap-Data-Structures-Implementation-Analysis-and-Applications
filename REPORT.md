# Assignment 4: Heap Data Structures: Implementation, Analysis, and Applications

## 1. Heapsort implementation

`heapsort.py` stores a complete binary max-heap in the input list. For an element at index `i`, its children are `2i + 1` and `2i + 2`; the parent is `(i - 1) // 2`. The algorithm first heapifies the list bottom-up, starting at the last internal node. It then swaps the root (the maximum) with the last item in the active heap, shrinks the heap by one, and sifts the new root down. Repeating this leaves the values in ascending order. The function sorts in place and returns the same sequence.

### Complexity

Bottom-up heap construction is Θ(n), rather than Θ(n log n): nodes near the leaves require little or no sifting, and summing each node's possible height over the complete tree is linear. There are n−1 extractions; restoring the heap takes O(log n) in the worst case, yielding Θ(n log n) overall. The extraction work is Θ(n log n) for heapsort across best, average, and worst input arrangements: the algorithm continues removing maxima and restoring the complete heap regardless of the input order. Input arrangement can change the number of swaps/comparisons in individual sifts, but does not give heapsort a linear best case. Thus the best, average, and worst asymptotic time bounds are all Θ(n log n).

The algorithm uses Θ(1) auxiliary space: swaps and a constant number of indices are used, with no recursion or second array. It is not stable; equal values may change relative order. Its practical overhead includes Python loop and comparison costs, and it may have poorer cache locality than algorithms that scan contiguous runs.

## 2. Sorting comparison

`benchmark.py` compares the submission's heapsort with an iterative randomized three-way quicksort and a stable top-down mergesort. Each data set is copied before a run; the result is checked against Python's sorted output. Inputs are deterministic, generated with seed 2026, and include random, sorted, and reverse-sorted orders at n = 1,000, 5,000, and 10,000. Each cell is the median of three runs measured with `time.perf_counter()`. Full raw results are in `benchmark_results.csv`.

| n | Distribution | Heapsort (s) | Quicksort (s) | Mergesort (s) |
|---:|---|---:|---:|---:|
| 1,000 | Random | 0.003305 | 0.003540 | 0.003390 |
| 1,000 | Sorted | 0.004505 | 0.003385 | 0.002198 |
| 1,000 | Reverse | 0.004209 | 0.003948 | 0.001792 |
| 5,000 | Random | 0.016708 | 0.017516 | 0.018554 |
| 5,000 | Sorted | 0.018557 | 0.013513 | 0.009043 |
| 5,000 | Reverse | 0.015438 | 0.013458 | 0.010685 |
| 10,000 | Random | 0.036161 | 0.033939 | 0.050821 |
| 10,000 | Sorted | 0.050812 | 0.048426 | 0.031650 |
| 10,000 | Reverse | 0.058590 | 0.046295 | 0.033363 |

All three exhibit broadly n log n scaling on these sizes. The observed times are not a ranking of abstract algorithms: these are different Python implementations with different allocation and interpreter overheads. Mergesort is especially simple on ordered runs but allocates intermediate lists. Quicksort uses random pivots and three-way partitioning, avoiding the classic sorted-input degeneration of deterministic first-element quicksort; its timing can still vary. Heapsort's in-place guarantee and worst-case bound are attractive, while Python-level sift operations can incur substantial interpreter overhead. Small timing differences should not be treated as statistically conclusive; the benchmark is intentionally a compact classroom comparison, not a controlled performance study.

## 3. Priority queue design

`priority_queue.py` uses a Python list for the complete binary max-heap and a dictionary mapping task IDs to current array indices. The list supports compact storage and O(1) parent/child index calculations. The map makes a task's heap position findable in O(1), so key changes can restore the heap in O(log n) without searching. The ordering uses larger numeric priority first, then earlier arrival time, then task ID as a deterministic final tie-breaker. Duplicate task IDs are rejected.

| Operation | Complexity | Explanation |
|---|---:|---|
| `insert(task)` | O(log n) | Append then bubble up; map maintenance is O(1) per swap. |
| `extract_max()` | O(log n) | Remove root, move final item to root, sift down. |
| `increase_key(task_id, p)` | O(log n) | O(1) map lookup, then bubble up. |
| `decrease_key(task_id, p)` | O(log n) | O(1) map lookup, then sift down. |
| `is_empty()` | O(1) | Checks heap length. |
| Space | O(n) | Heap list and position map each hold O(n) entries. |

Increasing a key to a lower value or decreasing it to a higher value raises `ValueError`, keeping each method's precondition explicit. Unknown task IDs naturally raise `KeyError`; extracting from an empty queue raises `IndexError`.

## 4. Scheduler simulation

The simulation is a single-processor, non-preemptive priority scheduler. At each dispatch point it inserts all tasks that have arrived by the current time, then chooses the highest-priority available task. If no task is ready, time advances to the next arrival. The processor runs the selected task to completion; arrivals during execution become eligible at the next dispatch. Each returned record contains task ID, priority, start and finish times, deadline, and an `on_time` Boolean based on `finish <= deadline`.

For the included example (A: priority 2, arrival 0, duration 3; B: priority 5, arrival 1, duration 2; C: priority 3, arrival 2, duration 1), A starts at 0 and finishes at 3. B and C are then ready, so B runs from 3 to 5, followed by C from 5 to 6. With deadlines 5, 8, and 10 respectively, all finish on time. This illustrates the policy; it does not claim that priority scheduling optimizes deadline satisfaction. A newly arriving urgent task cannot interrupt work already in progress.

## 5. Reproduction and limitations

Run `python heapsort.py`, `python priority_queue.py`, and `python benchmark.py` from the submission directory. Timings reported above were collected in one local Python runtime; runtime, CPU, and background load affect them. The scheduler assumes integer time units and valid nonnegative durations, and does not model preemption, resource constraints, or task cancellation.
