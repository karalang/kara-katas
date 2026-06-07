"""LeetCode #24: Swap Nodes in Pairs — iterative O(n), O(1) extra.

Mirror of iterative.kara: a dummy-anchored cursor walk that re-links each
adjacent pair (prev → first → second → rest becomes prev → second → first →
rest) via three pointer stores, then advances `prev` to the back node of the
swapped pair. A trailing singleton on odd-length input stays in place.
Renders each result list one per line so this file diffs line-for-line
against the Kāra mirror across all nine cases.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def swap_pairs(head: Optional[ListNode]) -> Optional[ListNode]:
    # Dummy before the head: the first pair grafts onto `prev.next` like
    # every other pair, so swapping the head is not a special case.
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next is not None and prev.next.next is not None:
        first = prev.next
        second = first.next
        # Re-link prev → second → first → rest.
        first.next = second.next
        second.next = first
        prev.next = second
        prev = first
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


def report(arr: list[int]) -> None:
    print(to_string(swap_pairs(from_array(arr))))


def main() -> None:
    report([1, 2, 3, 4])        # [2, 1, 4, 3]
    report([])                  # []
    report([1])                 # [1]
    report([1, 2])              # [2, 1]
    report([1, 2, 3])           # [2, 1, 3]
    report([1, 2, 3, 4, 5])     # [2, 1, 4, 3, 5]
    report([1, 2, 3, 4, 5, 6])  # [2, 1, 4, 3, 6, 5]
    report([7, 7, 7, 7])        # [7, 7, 7, 7]
    report([100, 0, 99, 1])     # [0, 100, 1, 99]


if __name__ == "__main__":
    main()
