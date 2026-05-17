"""LeetCode #2: Add Two Numbers — recursive O(max(m, n)).

Mirrors recursive.kara line-for-line in shape and output so the two files
can be diffed directly.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def add_rec(a: Optional[ListNode], b: Optional[ListNode], carry: int) -> Optional[ListNode]:
    s = carry
    next_a: Optional[ListNode] = None
    next_b: Optional[ListNode] = None
    done = True
    if a is not None:
        s += a.val
        next_a = a.next
        done = False
    if b is not None:
        s += b.val
        next_b = b.next
        done = False
    if done and s == 0:
        return None
    return ListNode(s % 10, add_rec(next_a, next_b, s // 10))


def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    return add_rec(l1, l2, 0)


def from_array(arr: list[int]) -> Optional[ListNode]:
    result: Optional[ListNode] = None
    for v in reversed(arr):
        result = ListNode(v, result)
    return result


def to_string(list_: Optional[ListNode]) -> str:
    parts: list[str] = []
    current = list_
    while current is not None:
        parts.append(str(current.val))
        current = current.next
    return "[" + ", ".join(parts) + "]"


def report(a: list[int], b: list[int]) -> None:
    print(to_string(add_two_numbers(from_array(a), from_array(b))))


def main() -> None:
    # 342 + 465 = 807
    report([2, 4, 3], [5, 6, 4])

    # 0 + 0 = 0
    report([0], [0])

    # 9999999 + 9999 = 10009998
    report([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9])

    # 1 + 99 = 100 — pure carry-propagation case
    report([1], [9, 9])

    # 5 + 5 = 10 — carry produces an extra leading digit
    report([5], [5])

    # 7 + 0 = 7 — single-digit, no carry
    report([7], [0])


if __name__ == "__main__":
    main()
