"""Benchmark workload — Rotate List (LeetCode #61).

Python mirror of bench/rotate_list.kara. Same append list-builder, close-the-
ring rotation, rotation sweep r = k % (2*N), and sink shape. CPython is
multi-second per sample at the compiled mirrors' K=500_000, so this runs
K=100_000 (1/5th) and the README quotes the projected ratio. span=200 divides
100_000 evenly, so the sweep covers every rotation the same number of times;
sink = 5_050_000 (one fifth of the compiled mirrors' 25_250_000).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def rotate_right(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    length = 0
    cur = head
    tail: Optional[ListNode] = None
    while cur is not None:
        length += 1
        tail = cur
        cur = cur.next

    if length == 0:
        return None
    shift = k % length
    if shift == 0:
        return head

    if tail is not None:
        tail.next = head  # close the ring

    steps = length - shift - 1
    new_tail = head
    for _ in range(steps):
        if new_tail is not None:
            new_tail = new_tail.next

    result = head
    if new_tail is not None:
        result = new_tail.next
        new_tail.next = None  # sever the ring
    return result


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
    span = 200  # 2*N
    k_iters = 100_000

    total = 0
    for k in range(k_iters):
        lst = build_list(n_values)
        r = k % span
        out = rotate_right(lst, r)
        if out is not None:
            total += out.val
    print(total)


if __name__ == "__main__":
    main()
