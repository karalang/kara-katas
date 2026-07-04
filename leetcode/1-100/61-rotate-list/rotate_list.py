"""LeetCode #61: Rotate List — close-the-ring then cut.

Mirror of rotate_list.kara: measure the length L and find the tail, reduce
`k` modulo L, join tail -> head into a ring, walk (L - s - 1) steps to the new
tail, and sever the ring right after it. Same output format (the result list
rendered one per line) so the two files diff line-for-line across all ten
cases.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def rotate_right(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    # One pass: count the nodes (L) and hold onto the tail.
    length = 0
    cur = head
    tail: Optional[ListNode] = None
    while cur is not None:
        length += 1
        tail = cur
        cur = cur.next

    # Empty list, or a rotation that is a whole multiple of the length: no-op.
    if length == 0:
        return None
    shift = k % length
    if shift == 0:
        return head

    # Close the ring, walk to the new tail, then sever right after it.
    if tail is not None:
        tail.next = head

    steps = length - shift - 1
    new_tail = head
    for _ in range(steps):
        if new_tail is not None:
            new_tail = new_tail.next

    result = head
    if new_tail is not None:
        result = new_tail.next
        new_tail.next = None
    return result


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


def report(arr: list[int], k: int) -> None:
    head = from_array(arr)
    out = rotate_right(head, k)
    print(to_string(out))


def main() -> None:
    report([1, 2, 3, 4, 5], 2)            # [4, 5, 1, 2, 3]
    report([0, 1, 2], 4)                  # [2, 0, 1]
    report([], 0)                         # []
    report([], 3)                         # []
    report([1], 99)                       # [1]
    report([1, 2], 1)                     # [2, 1]
    report([1, 2], 2)                     # [1, 2]
    report([1, 2, 3], 2000000000)         # [2, 3, 1]
    report([1, 2, 3, 4, 5], 5)            # [1, 2, 3, 4, 5]
    report([1, 2, 3, 4, 5], 7)            # [4, 5, 1, 2, 3]


if __name__ == "__main__":
    main()
