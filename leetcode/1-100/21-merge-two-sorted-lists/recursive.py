"""LeetCode #21: Merge Two Sorted Lists — recursive O(m + n).

Mirror of recursive.kara: pick the smaller front node and set its `next` to
the merge of the rest; the base cases (one list empty) return the other list
whole. `<=` on the tie keeps the merge stable. Same nine cases and one-per-
line output as iterative.py, so all three (iterative.kara / recursive.kara /
this file) diff line-for-line.
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
    if l1 is None:
        return l2
    if l2 is None:
        return l1
    # `<=` keeps the merge stable (list-1 node wins a tie).
    if l1.val <= l2.val:
        l1.next = merge_two_lists(l1.next, l2)
        return l1
    l2.next = merge_two_lists(l1, l2.next)
    return l2


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
