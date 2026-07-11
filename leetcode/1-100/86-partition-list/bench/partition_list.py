"""Benchmark workload — Partition List (LeetCode #86), SEQ lane.

Python mirror of bench/partition_list.kara. Each iteration builds a fresh M=200 list,
stably partitions around x=50, and adds the fold into an associative sum. Runs a
smaller K (pure-Python is slow); timed separately, NOT cross-checked. See ../README.md.
"""

from __future__ import annotations

from typing import Optional


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val: int, nxt: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = nxt


def partition(head: Optional[ListNode], x: int) -> Optional[ListNode]:
    less_dummy = ListNode(0)
    greater_dummy = ListNode(0)
    less_tail = less_dummy
    greater_tail = greater_dummy
    cur = head
    while cur is not None:
        nxt = cur.next
        cur.next = None
        if cur.val < x:
            less_tail.next = cur
            less_tail = cur
        else:
            greater_tail.next = cur
            greater_tail = cur
        cur = nxt
    less_tail.next = greater_dummy.next
    return less_dummy.next


def build(m: int, seed: int) -> Optional[ListNode]:
    dummy = ListNode(-1)
    tail = dummy
    for j in range(m):
        node = ListNode((j * 7 + seed) % 100)
        tail.next = node
        tail = node
    return dummy.next


def fold(list_: Optional[ListNode], seed: int) -> int:
    a = seed
    c = list_
    while c is not None:
        a = (a * 131 + (c.val + 1000)) % 1000000007
        c = c.next
    return a


def main() -> None:
    m = 200
    total = 8000
    total_sum = 0
    for k in range(total):
        list_ = build(m, k)
        p = partition(list_, 50)
        total_sum += fold(p, k)
    print(total_sum)


if __name__ == "__main__":
    main()
