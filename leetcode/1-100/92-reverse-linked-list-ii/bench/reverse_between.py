"""Benchmark workload — Reverse Linked List II (LeetCode #92).

Python mirror of bench/reverse_between.kara. Each iteration builds a fresh M=200 list,
reverses a ~100-node window (shifting start), folds the result. Smaller K (pure-Python
is slow); timed separately, NOT cross-checked. See ../README.md.
"""

from typing import Optional


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val: int, nxt: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = nxt


def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(1, left):
        if prev.next:
            prev = prev.next
    cur = prev.next
    if cur:
        for _ in range(left, right):
            nxt = cur.next
            if nxt:
                cur.next = nxt.next
                nxt.next = prev.next
                prev.next = nxt
    return dummy.next


def build(m, seed):
    dummy = ListNode(-1)
    tail = dummy
    for j in range(m):
        node = ListNode((j + seed) % 1000)
        tail.next = node
        tail = node
    return dummy.next


def fold(list_, seed):
    a = seed
    c = list_
    while c is not None:
        a = (a * 131 + (c.val + 1000)) % 1000000007
        c = c.next
    return a


def main():
    m = 200
    total = 6000
    modulus = 1000000007
    total_sum = 0
    for k in range(total):
        list_ = build(m, k)
        left = 1 + (k % 50)
        right = left + 100
        r = reverse_between(list_, left, right)
        total_sum = (total_sum * 131 + fold(r, k)) % modulus
    print(total_sum)


if __name__ == "__main__":
    main()
