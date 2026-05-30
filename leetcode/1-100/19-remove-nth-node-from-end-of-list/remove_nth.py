"""LeetCode #19: Remove Nth Node From End of List — one-pass two-pointer.

Mirror of remove_nth.kara: same dummy-anchored gap two-pointer (advance
`fast` n nodes, then walk `fast`/`slow` in lockstep until `fast` falls off
the end, then splice `slow.next`), and the same output format (the result
list rendered one per line) so the two files diff line-for-line across all
eight cases.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)

    # Step 1 — lead `fast` n nodes into the list from the head.
    fast = head
    for _ in range(n):
        if fast is not None:
            fast = fast.next

    # Step 2 — walk `slow` (from the dummy) and `fast` in lockstep until
    # `fast` runs off the end. `slow` then rests just before the target.
    slow = dummy
    while fast is not None:
        fast = fast.next
        if slow.next is not None:
            slow = slow.next

    # Step 3 — splice out `slow.next` (the n-th node from the end).
    if slow.next is not None:
        slow.next = slow.next.next

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


def report(arr: list[int], n: int) -> None:
    head = from_array(arr)
    out = remove_nth_from_end(head, n)
    print(to_string(out))


def main() -> None:
    report([1, 2, 3, 4, 5], 2)   # [1, 2, 3, 5]
    report([1], 1)               # []
    report([1, 2], 1)            # [1]
    report([1, 2], 2)            # [2]
    report([1, 2, 3, 4, 5], 5)   # [2, 3, 4, 5]
    report([1, 2, 3, 4, 5], 1)   # [1, 2, 3, 4]
    report([1, 2, 3, 4, 5], 3)   # [1, 2, 4, 5]
    report([7, 8, 9], 3)         # [8, 9]


if __name__ == "__main__":
    main()
