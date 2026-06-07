"""LeetCode #23: Merge k Sorted Lists — k-way merge with a binary min-heap
of cursors, O(N log k).

Mirror of heap.kara: a hand-rolled binary min-heap over a list of nodes
(same shape as the Kāra mirror, which has no stdlib heap to call — heapq is
deliberately not used), keyed on the cursor node's value. Pop the global
minimum, splice it onto the output tail, push its successor. Renders each
result list one per line so this file diffs line-for-line against the Kāra
mirror across all ten cases.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def heap_push(heap: list[ListNode], node: ListNode) -> None:
    heap.append(node)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[i].val < heap[parent].val:
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            break


def heap_pop(heap: list[ListNode]) -> ListNode:
    top = heap[0]
    last = heap.pop()
    if heap:
        # `last` was not the root itself — re-seat it and sift down.
        heap[0] = last
        m = len(heap)
        i = 0
        while True:
            l = 2 * i + 1
            r = l + 1
            smallest = i
            if l < m and heap[l].val < heap[smallest].val:
                smallest = l
            if r < m and heap[r].val < heap[smallest].val:
                smallest = r
            if smallest == i:
                break
            heap[i], heap[smallest] = heap[smallest], heap[i]
            i = smallest
    return top


def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    # Seed the frontier: one cursor per non-empty list.
    heap: list[ListNode] = []
    for head in lists:
        if head is not None:
            heap_push(heap, head)

    # Pop the global minimum, splice it, advance its list's cursor.
    dummy = ListNode(0)
    tail = dummy
    while heap:
        node = heap_pop(heap)
        tail.next = node
        tail = node
        if node.next is not None:
            heap_push(heap, node.next)
    return dummy.next


def from_array(arr: list[int]) -> Optional[ListNode]:
    head: Optional[ListNode] = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head


def to_string(list_: Optional[ListNode]) -> str:
    parts: list[str] = []
    current = list_
    while current is not None:
        parts.append(str(current.val))
        current = current.next
    return "[" + ", ".join(parts) + "]"


def report(arrays: list[list[int]]) -> None:
    print(to_string(merge_k_lists([from_array(a) for a in arrays])))


def main() -> None:
    report([[1, 4, 5], [1, 3, 4], [2, 6]])      # [1, 1, 2, 3, 4, 4, 5, 6]
    report([])                                  # []
    report([[]])                                # []
    report([[1, 2, 3]])                         # [1, 2, 3]
    report([[], [1], []])                       # [1]
    report([[7, 8, 9], [1, 2, 3], [4, 5, 6]])   # [1, 2, 3, 4, 5, 6, 7, 8, 9]
    report([[2, 2], [2], [2, 2, 2]])            # [2, 2, 2, 2, 2, 2]
    report([[-10, -5, 0], [-7, 3], [-6, -6]])   # [-10, -7, -6, -6, -5, 0, 3]
    report([[5], [1, 6], [3], [2, 7], [4], [0]])  # [0, 1, 2, 3, 4, 5, 6, 7]
    report([[1, 10, 20], [2], [3, 4, 5, 6, 7]])  # [1, 2, 3, 4, 5, 6, 7, 10, 20]


if __name__ == "__main__":
    main()
