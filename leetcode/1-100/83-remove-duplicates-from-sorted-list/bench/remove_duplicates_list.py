"""Benchmark workload — Remove Duplicates from Sorted List (LeetCode #83).

Python mirror of bench/remove_duplicates_list.kara. Each iteration builds a fresh
sorted list (M=300, every value duplicated), runs the keep-one dedup, and folds the
survivors through a rolling polynomial hash. Runs a smaller K (pure-Python is slow);
timed separately, NOT cross-checked. See ../README.md.
"""

from __future__ import annotations

from typing import Optional


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val: int, nxt: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = nxt


def delete_duplicates(head: Optional[ListNode]) -> Optional[ListNode]:
    cur = head
    while cur is not None:
        if cur.next is not None:
            if cur.val == cur.next.val:
                cur.next = cur.next.next
            else:
                cur = cur.next
        else:
            break
    return head


def build(m: int, dup: int) -> Optional[ListNode]:
    dummy = ListNode(-1)
    tail = dummy
    for v in range(m):
        for _ in range(dup):
            node = ListNode(v)
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
    m = 300
    dup = 2
    total = 3500
    modulus = 1000000007
    total_sum = 0
    for k in range(total):
        list_ = build(m, dup)
        dd = delete_duplicates(list_)
        total_sum = (total_sum * 131 + fold(dd, k)) % modulus
    print(total_sum)


if __name__ == "__main__":
    main()
