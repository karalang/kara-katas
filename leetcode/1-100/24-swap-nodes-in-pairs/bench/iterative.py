"""Benchmark workload — Swap Nodes in Pairs (LeetCode #24), iterative.

Python mirror of bench/iterative.kara at K=100_000 (one fifth of the compiled
mirrors' K=500_000 — CPython is the ergonomic-foil lane, timed separately and
scaled in the README). Same N, same build + in-place pair re-link +
full-traversal sink shape. Plain `@dataclass` node, matching the kata-2/19/21
linked-list mirrors (no `__slots__` — corpus-uniform methodology).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def swap_pairs(head):
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


def build_list(count: int):
    head = None
    for v in range(count, 0, -1):
        head = ListNode(v, head)
    return head


def sum_list(list_):
    s = 0
    c = list_
    while c is not None:
        s += c.val
        c = c.next
    return s


def main() -> None:
    n_values = 100
    k_iters = 100_000

    total = 0
    for _ in range(k_iters):
        lst = build_list(n_values)
        total += sum_list(swap_pairs(lst))
    print(total)


if __name__ == "__main__":
    main()
