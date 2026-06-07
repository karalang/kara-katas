"""Benchmark workload — Merge k Sorted Lists (LeetCode #23), divide and
conquer. Python mirror of bench/divide_and_conquer.kara, run at a scaled-down
K (CPython is the ergonomic-foil lane, timed separately — not in the compiled
cross-check). Same stride-k interleaving build, pairwise interval merge, and
full-traversal sink. See ../README.md § Benchmarks.
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


def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    k = len(lists)
    if k == 0:
        return None
    interval = 1
    while interval < k:
        for i in range(0, k - interval, 2 * interval):
            lists[i] = merge_two_lists(lists[i], lists[i + interval])
        interval *= 2
    return lists[0]


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
    k_lists = 8
    n_values = 128
    k_iters = 10_000  # scaled down from the compiled mirrors' 100k

    total = 0
    for _ in range(k_iters):
        lists = [build_list(j, k_lists, n_values) for j in range(k_lists)]
        total += sum_list(merge_k_lists(lists))
    print(total)


if __name__ == "__main__":
    main()
