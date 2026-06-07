"""Benchmark workload — Reverse Nodes in k-Group (LeetCode #25), iterative.

Python mirror of bench/iterative.kara at K=100_000 (one fifth of the compiled
mirrors' K=500_000 — CPython is the ergonomic-foil lane, timed separately and
scaled in the README). Same N, same k=5, same build + in-place group reversal
+ full-traversal sink shape. Plain `@dataclass` node, matching the
kata-2/19/21/24 linked-list mirrors (no `__slots__` — corpus-uniform
methodology).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        # Probe k nodes ahead; a partial trailing group stays in place.
        probe = group_prev.next
        count = 0
        while count < k and probe is not None:
            probe = probe.next
            count += 1
        if count < k:
            break
        group_head = group_prev.next
        # Reverse exactly k nodes, prev seeded with the suffix.
        prev = probe
        cur = group_prev.next
        for _ in range(k):
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        group_prev.next = prev
        group_prev = group_head
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
        total += sum_list(reverse_k_group(lst, 5))
    print(total)


if __name__ == "__main__":
    main()
