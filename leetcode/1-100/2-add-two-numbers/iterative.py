"""LeetCode #2: Add Two Numbers — iterative O(max(m, n)).

Mirrors iterative.kara line-for-line in shape and output so the two files
can be diffed directly.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    digits: list[int] = []
    a, b = l1, l2
    carry = 0

    while True:
        if a is None and b is None:
            if carry != 0:
                digits.append(carry)
            break
        if a is not None and b is None:
            s = a.val + carry
            digits.append(s % 10)
            carry = s // 10
            a = a.next
        elif a is None and b is not None:
            s = b.val + carry
            digits.append(s % 10)
            carry = s // 10
            b = b.next
        else:
            s = a.val + b.val + carry
            digits.append(s % 10)
            carry = s // 10
            a = a.next
            b = b.next

    out: Optional[ListNode] = None
    for d in reversed(digits):
        out = ListNode(d, out)
    return out


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
