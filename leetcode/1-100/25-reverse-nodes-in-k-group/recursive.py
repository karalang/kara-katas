"""LeetCode #25: Reverse Nodes in k-Group — recursive O(n), O(n/k) stack.

Mirror of recursive.kara: each call probes k nodes ahead (fewer than k →
return the suffix unchanged), recurses on the rest first, then reverses its
own k nodes onto the already-reversed tail with the same prev/cur pointer
loop, returning the old k-th node as the new group head. Renders each result
list one per line so this file diffs line-for-line against the Kāra mirror
across all nine cases.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import sys


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    # Probe: does a full group of k nodes start at `head`?
    probe = head
    count = 0
    while count < k:
        if probe is None:
            # Fewer than k remain — the partial suffix stays as-is.
            return head
        probe = probe.next
        count += 1

    # Recurse on the rest first, then reverse the local k nodes onto the
    # already-reversed tail.
    prev = reverse_k_group(probe, k)
    cur = head
    for _ in range(k):
        assert cur is not None
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    # `prev` is the old k-th node — the new group head.
    return prev


def from_array(arr: list[int]) -> Optional[ListNode]:
    head: Optional[ListNode] = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head


def to_string(list_: Optional[ListNode]) -> str:
    parts: list[str] = []
    current = list_
    while current is not None:
        parts.append(str(current.val))
        current = current.next
    return "[" + ", ".join(parts) + "]"


def report(arr: list[int], k: int) -> None:
    print(to_string(reverse_k_group(from_array(arr), k)))


def main() -> None:
    # Depth n/k frames; k = 1 over 5000 nodes would exceed CPython's default
    # 1000-frame limit — the test cases stay tiny, but mirror honestly.
    sys.setrecursionlimit(10_000)
    report([1, 2, 3, 4, 5], 2)           # [2, 1, 4, 3, 5]
    report([1, 2, 3, 4, 5], 3)           # [3, 2, 1, 4, 5]
    report([1], 1)                       # [1]
    report([1, 2, 3, 4, 5], 1)           # [1, 2, 3, 4, 5]
    report([1, 2, 3, 4, 5], 5)           # [5, 4, 3, 2, 1]
    report([1, 2, 3, 4, 5, 6], 2)        # [2, 1, 4, 3, 6, 5]
    report([1, 2, 3, 4, 5, 6, 7, 8], 4)  # [4, 3, 2, 1, 8, 7, 6, 5]
    report([7, 7, 7, 7], 2)              # [7, 7, 7, 7]
    report([1000, 0, 999, 1, 500], 3)    # [999, 0, 1000, 1, 500]


if __name__ == "__main__":
    main()
