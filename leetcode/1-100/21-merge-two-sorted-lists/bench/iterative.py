"""Benchmark workload — Merge Two Sorted Lists (LeetCode #21), iterative.

Python mirror of bench/iterative.kara, run at a scaled-down K (CPython is the
ergonomic-foil lane, timed separately — not in the compiled cross-check). Same
evens/odds interleaving build, dummy-anchored splice, and full-traversal sink.
See ../README.md § Benchmarks.
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


def build_list(start: int, step: int, count: int) -> Optional[ListNode]:
    if count <= 0:
        return None
    head = ListNode(start)
    tail = head
    v = start
    for _ in range(1, count):
        v += step
        node = ListNode(v)
        tail.next = node
        tail = node
    return head


def sum_list(list_: Optional[ListNode]) -> int:
    s = 0
    c = list_
    while c is not None:
        s += c.val
        c = c.next
    return s


def main() -> None:
    n_values = 100
    k_iters = 100_000  # scaled down from the compiled mirrors' 500k

    total = 0
    for _ in range(k_iters):
        a = build_list(0, 2, n_values)
        b = build_list(1, 2, n_values)
        total += sum_list(merge_two_lists(a, b))
    print(total)


if __name__ == "__main__":
    main()
