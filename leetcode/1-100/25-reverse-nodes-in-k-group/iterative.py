"""LeetCode #25: Reverse Nodes in k-Group — iterative O(n), O(1) extra.

Mirror of iterative.kara: a dummy-anchored group walk. Each round probes k
nodes ahead (a partial trailing group stays in original order), reverses the
group with the standard prev/cur pointer loop seeded on the suffix, grafts it
back via group_prev, and advances the anchor to the old group head (the new
tail). Renders each result list one per line so this file diffs line-for-line
against the Kāra mirror across all nine cases.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    # Dummy before the head: the first group grafts onto `group_prev.next`
    # like every other group, so reversing the head group is not special.
    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        # Step 1 — probe k nodes ahead; stop if the list runs out first.
        probe = group_prev.next
        count = 0
        while count < k and probe is not None:
            probe = probe.next
            count += 1
        if count < k:
            break

        # Step 2 — reverse exactly k nodes; `prev` seeds with the suffix so
        # the old group head (the new tail) links straight to it.
        group_head = group_prev.next
        assert group_head is not None
        prev = probe
        cur: Optional[ListNode] = group_head
        for _ in range(k):
            assert cur is not None
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        # Step 3 — graft and advance the anchor to the old group head.
        group_prev.next = prev
        group_prev = group_head

    return dummy.next


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
