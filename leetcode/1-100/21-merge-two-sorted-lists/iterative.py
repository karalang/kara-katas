"""LeetCode #21: Merge Two Sorted Lists — iterative O(m + n), O(1) extra.

Mirror of iterative.kara: the same dummy-anchored splice — walk both lists,
splice the smaller front node onto a growing tail, graft the surviving suffix
when one list runs dry. `<=` on the tie keeps the merge stable. Renders each
result list one per line so this file diffs line-for-line against the Kāra
mirror across all nine cases.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def merge_two_lists(
    l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    # Dummy before the output head: the first spliced node is `dummy.next`.
    dummy = ListNode(0)
    tail = dummy
    a, b = l1, l2
    while a is not None and b is not None:
        # `<=` keeps the merge stable on ties (list-1 node wins).
        if a.val <= b.val:
            tail.next = a
            tail = a
            a = a.next
        else:
            tail.next = b
            tail = b
            b = b.next
    # One list is exhausted — graft what remains of the other in one move.
    tail.next = a if a is not None else b
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


def report(a: list[int], b: list[int]) -> None:
    print(to_string(merge_two_lists(from_array(a), from_array(b))))


def main() -> None:
    report([1, 2, 4], [1, 3, 4])    # [1, 1, 2, 3, 4, 4]
    report([], [])                  # []
    report([], [0])                 # [0]
    report([5], [])                 # [5]
    report([1, 2, 3], [4, 5, 6])    # [1, 2, 3, 4, 5, 6]
    report([4, 5, 6], [1, 2, 3])    # [1, 2, 3, 4, 5, 6]
    report([2, 2, 2], [2, 2])       # [2, 2, 2, 2, 2]
    report([1], [2])                # [1, 2]
    report([-3, -1, 2], [-2, 0, 4])  # [-3, -2, -1, 0, 2, 4]


if __name__ == "__main__":
    main()
