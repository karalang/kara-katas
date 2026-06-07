"""LeetCode #24: Swap Nodes in Pairs — recursive O(n), O(n/2) stack.

Mirror of recursive.kara: structural recursion two nodes at a time —
swap(first → second → rest) = second → first → swap(rest); a zero- or
one-node suffix returns unchanged. Renders each result list one per line so
this file diffs line-for-line against the Kāra mirror across all nine cases.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def swap_pairs(head: Optional[ListNode]) -> Optional[ListNode]:
    if head is None or head.next is None:
        # Empty suffix or trailing singleton — already "swapped".
        return head
    first = head
    second = head.next
    # Swap the front pair; the recursion has already swapped `rest`.
    first.next = swap_pairs(second.next)
    second.next = first
    return second


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
