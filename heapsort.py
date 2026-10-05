"""In-place heapsort for comparable Python values."""

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def heapsort(values: MutableSequence[T]) -> MutableSequence[T]:
    """Sort values in ascending order in place and return the same sequence.

    The active heap occupies values[0:end]. Building it bottom-up is O(n);
    each of the n removals restores the max-heap in O(log n).
    """
    n = len(values)

    def sift_down(root: int, end: int) -> None:
        while 2 * root + 1 < end:
            child = 2 * root + 1
            right = child + 1
            if right < end and values[child] < values[right]:
                child = right
            if not values[root] < values[child]:
                return
            values[root], values[child] = values[child], values[root]
            root = child

    for root in range(n // 2 - 1, -1, -1):
        sift_down(root, n)
    for end in range(n - 1, 0, -1):
        values[0], values[end] = values[end], values[0]
        sift_down(0, end)
    return values


if __name__ == "__main__":
    sample = [12, 3, 5, 7, 19, 1]
    heapsort(sample)
    print(sample)
