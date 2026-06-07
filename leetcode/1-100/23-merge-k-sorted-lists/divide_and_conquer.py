"""LeetCode #23: Merge k Sorted Lists — divide and conquer, O(N log k).

Mirror of divide_and_conquer.kara: kata #21's iterative two-list merge as the
inner kernel, driven by the in-place interval walk — round with interval d
merges slot i with slot i+d for i = 0, 2d, 4d, …, so log k rounds each touch
every live node once. Source slots are consumed once and left stale; the
answer ends in slot 0. Renders each result list one per line so this file
diffs line-for-line against the Kāra mirror across all ten cases.
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
    # Kata #21's dummy-anchored splice; `<=` keeps each pairwise merge stable.
    dummy = ListNode(0)
    tail = dummy
    a, b = l1, l2
    while a is not None and b is not None:
        if a.val <= b.val:
            tail.next = a
            tail = a
            a = a.next
        else:
            tail.next = b
            tail = b
            b = b.next
    tail.next = a if a is not None else b
    return dummy.next


def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    k = len(lists)
    if k == 0:
        return None
    interval = 1
    while interval < k:
        for i in range(0, k - interval, 2 * interval):
            lists[i] = merge_two_lists(lists[i], lists[i + interval])
        interval *= 2
    return lists[0]


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
