"""LeetCode #2 bench mirror — algorithmic peer of iterative.kara.

N=100 digit lists, K=500_000 iterations of add_two_numbers. Sink is sum
of the first digit of each result.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0)
    tail = dummy
    a, b = l1, l2
    carry = 0
    while True:
        s = carry
        done = True
        if a is not None:
            s += a.val
            a = a.next
            done = False
        if b is not None:
            s += b.val
            b = b.next
            done = False
        if done and s == 0:
            break
        node = ListNode(s % 10)
        tail.next = node
        tail = node
        carry = s // 10
    return dummy.next


def from_array(arr: list[int]) -> Optional[ListNode]:
    head: Optional[ListNode] = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head


def main() -> None:
    N = 100
    K = 500_000

    a = [9] * N
    b = [9] * N
    l1 = from_array(a)
    l2 = from_array(b)

    sum_ = 0
    for _ in range(K):
        out = add_two_numbers(l1, l2)
        if out is not None:
            sum_ += out.val
    print(sum_)


if __name__ == "__main__":
    main()
