"""Reproducible comparison of heapsort, quicksort, and mergesort."""

import random
import statistics
import time
from typing import Callable, List

from heapsort import heapsort


def quicksort(a: List[int]) -> List[int]:
    """In-place iterative randomized three-way quicksort."""
    if len(a) < 2:
        return a
    stack = [(0, len(a) - 1)]
    rng = random.Random(42)
    while stack:
        lo, hi = stack.pop()
        while lo < hi:
            pivot = a[rng.randrange(lo, hi + 1)]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if a[i] < pivot:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif a[i] > pivot:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1
                else:
                    i += 1
            left, right = (lo, lt - 1), (gt + 1, hi)
            # Iterate on the smaller side; stack the larger to bound stack depth.
            if left[1] - left[0] < right[1] - right[0]:
                if right[0] < right[1]: stack.append(right)
                lo, hi = left
            else:
                if left[0] < left[1]: stack.append(left)
                lo, hi = right
    return a


def mergesort(a: List[int]) -> List[int]:
    """Top-down stable mergesort returning a new list."""
    if len(a) < 2:
        return a[:]
    mid = len(a) // 2
    left, right = mergesort(a[:mid]), mergesort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


SORTS: dict[str, Callable[[List[int]], List[int]]] = {
    "Heapsort": lambda x: heapsort(x),
    "Quicksort": quicksort,
    "Mergesort": mergesort,
}


def benchmark(sizes=(1000, 5000, 10000), repeats=3):
    rng = random.Random(2026)
    results = []
    for size in sizes:
        base = [rng.randrange(size * 10) for _ in range(size)]
        distributions = {"random": base, "sorted": sorted(base), "reverse": sorted(base, reverse=True)}
        for distribution, values in distributions.items():
            for name, sort in SORTS.items():
                timings = []
                for _ in range(repeats):
                    data = values.copy()
                    start = time.perf_counter()
                    result = sort(data)
                    timings.append(time.perf_counter() - start)
                    if result != sorted(values):
                        raise AssertionError(f"{name} failed on {distribution}, n={size}")
                results.append((size, distribution, name, statistics.median(timings)))
    return results


if __name__ == "__main__":
    print("n,distribution,algorithm,median_seconds")
    for row in benchmark():
        print(f"{row[0]},{row[1]},{row[2]},{row[3]:.6f}")
