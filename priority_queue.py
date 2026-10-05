"""Indexed binary max-heap and a small arrival/deadline scheduler demo."""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Task:
    task_id: str
    priority: int
    arrival_time: int
    deadline: int
    duration: int


class PriorityQueue:
    """Max-heap; larger priority wins, ties go to earlier arrivals then IDs."""

    def __init__(self) -> None:
        self._heap: List[Task] = []
        self._positions: Dict[str, int] = {}

    @staticmethod
    def _key(task: Task):
        return task.priority, -task.arrival_time, task.task_id

    def __len__(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return not self._heap

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._positions[self._heap[i].task_id] = i
        self._positions[self._heap[j].task_id] = j

    def _up(self, i: int) -> None:
        while i:
            parent = (i - 1) // 2
            if self._key(self._heap[parent]) >= self._key(self._heap[i]):
                break
            self._swap(parent, i)
            i = parent

    def _down(self, i: int) -> None:
        n = len(self._heap)
        while 2 * i + 1 < n:
            child = 2 * i + 1
            if child + 1 < n and self._key(self._heap[child + 1]) > self._key(self._heap[child]):
                child += 1
            if self._key(self._heap[i]) >= self._key(self._heap[child]):
                break
            self._swap(i, child)
            i = child

    def insert(self, task: Task) -> None:
        if task.task_id in self._positions:
            raise ValueError(f"duplicate task ID: {task.task_id}")
        self._positions[task.task_id] = len(self._heap)
        self._heap.append(task)
        self._up(len(self._heap) - 1)

    def extract_max(self) -> Task:
        if self.is_empty():
            raise IndexError("extract_max from an empty priority queue")
        maximum = self._heap[0]
        last = self._heap.pop()
        del self._positions[maximum.task_id]
        if self._heap:
            self._heap[0] = last
            self._positions[last.task_id] = 0
            self._down(0)
        return maximum

    def increase_key(self, task_id: str, new_priority: int) -> None:
        i = self._positions[task_id]
        if new_priority < self._heap[i].priority:
            raise ValueError("increase_key cannot lower priority")
        self._heap[i].priority = new_priority
        self._up(i)

    def decrease_key(self, task_id: str, new_priority: int) -> None:
        i = self._positions[task_id]
        if new_priority > self._heap[i].priority:
            raise ValueError("decrease_key cannot raise priority")
        self._heap[i].priority = new_priority
        self._down(i)


def simulate(tasks: List[Task]):
    """Non-preemptive single-processor schedule; returns completion records."""
    pending = sorted(tasks, key=lambda task: task.arrival_time)
    queue = PriorityQueue()
    now = 0
    next_task = 0
    records = []
    while next_task < len(pending) or not queue.is_empty():
        while next_task < len(pending) and pending[next_task].arrival_time <= now:
            queue.insert(pending[next_task])
            next_task += 1
        if queue.is_empty():
            now = pending[next_task].arrival_time
            continue
        task = queue.extract_max()
        start, finish = now, now + task.duration
        records.append({"task_id": task.task_id, "priority": task.priority,
                        "start": start, "finish": finish,
                        "deadline": task.deadline,
                        "on_time": finish <= task.deadline})
        now = finish
    return records


if __name__ == "__main__":
    sample = [Task("A", 2, 0, 5, 3), Task("B", 5, 1, 8, 2),
              Task("C", 3, 2, 10, 1)]
    for record in simulate(sample):
        print(record)
