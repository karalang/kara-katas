"""Benchmark workload — Remove Duplicates from Sorted List II (LeetCode #82).

Python mirror of bench/remove_duplicates_ii_list.kara. Each iteration builds a fresh
sorted list (even values duplicated, odd values single), runs delete_duplicates, and
folds the survivors through a rolling polynomial hash. Runs a smaller K (pure-Python
is slow); timed separately, NOT cross-checked. See ../README.md.
"""

from __future__ import annotations

from typing import Optional


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val: int, nxt: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = nxt


def delete_duplicates(head: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    prev = dummy
    cur = dummy.next
    while cur is not None:
        is_dup = cur.next is not None and cur.val == cur.next.val
        if is_dup:
            v = cur.val
            runner = cur
            while runner is not None and runner.val == v:
                runner = runner.next
            prev.next = runner
            cur = runner
        else:
            prev = cur
            cur = cur.next
    return dummy.next


def build(m: int) -> Optional[ListNode]:
    dummy = ListNode(-1)
    tail = dummy
    for v in range(m):
        node = ListNode(v)
        tail.next = node
        tail = node
        if v % 2 == 0:
            d = ListNode(v)
            tail.next = d
            tail = d
    return dummy.next


def fold(list_: Optional[ListNode], seed: int) -> int:
    a = seed
    c = list_
    while c is not None:
        a = (a * 131 + (c.val + 1000)) % 1000000007
        c = c.next
    return a


def main() -> None:
    m = 300
    total = 3000
    modulus = 1000000007
    total_sum = 0
    for k in range(total):
        list_ = build(m)
        dedup = delete_duplicates(list_)
        total_sum = (total_sum * 131 + fold(dedup, k)) % modulus
    print(total_sum)


if __name__ == "__main__":
    main()
