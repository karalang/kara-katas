"""Benchmark workload — Remove Nth Node From End (LeetCode #19).

Python mirror of bench/remove_nth.kara. Same append list-builder, two-pointer
removal, rotating position, and sink shape. CPython is multi-second per
sample at the compiled mirrors' K=500_000, so this runs K=100_000 (1/5th)
and the README quotes the projected ratio. M=100 divides 100_000 evenly, so
the rotation covers every removal position exactly 1000 times; the head is
removed on 1/100 of the iters (sink contribution 2 there, 1 elsewhere) →
sink = 99_000 + 2_000 = 101_000.
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

    fast = head
    for _ in range(n):
        if fast is not None:
            fast = fast.next

    slow = dummy
    while fast is not None:
        fast = fast.next
        if slow.next is not None:
            slow = slow.next

    if slow.next is not None:
        slow.next = slow.next.next

    return dummy.next


def build_list(count: int) -> Optional[ListNode]:
    if count <= 0:
        return None
    head = ListNode(1)
    tail = head
    for v in range(2, count + 1):
        node = ListNode(v)
        tail.next = node
        tail = node
    return head


def main() -> None:
    n_values = 100
    k_iters = 100_000

    total = 0
    for k in range(k_iters):
        lst = build_list(n_values)
        n = (k % n_values) + 1
        out = remove_nth_from_end(lst, n)
        if out is not None:
            total += out.val
    print(total)


if __name__ == "__main__":
    main()
