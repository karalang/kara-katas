"""LeetCode #86: Partition List — two-list split, stable, O(n).

Mirror of partition_list.kara. Thread nodes into a `less` list (val < x) and a
`greater` list (val >= x) as we walk, appending to each tail so both keep original
order (stability), then splice less -> greater. Each node is detached before
re-appending so no stale link makes a cycle. Same ten cases and output shape (an
`x=<x>: [...]` line per case, then a `sink:` fold of length + values) so the files
diff line-for-line.
"""

from __future__ import annotations

from typing import Optional


class ListNode:
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


def from_array(arr: list[int]) -> Optional[ListNode]:
    if not arr:
        return None
    head = ListNode(arr[0])
    tail = head
    for i in range(1, len(arr)):
        node = ListNode(arr[i])
        tail.next = node
        tail = node
    return head


def to_string(list_: Optional[ListNode]) -> str:
    parts = []
    cur = list_
    while cur is not None:
        parts.append(str(cur.val))
        cur = cur.next
    return "[" + ", ".join(parts) + "]"


def report(arr: list[int], x: int, acc: list[int]) -> None:
    out = partition(from_array(arr), x)
    print(f"x={x}: {to_string(out)}")
    a = acc[0]
    cur = out
    count = 0
    while cur is not None:
        a = (a * 131 + (cur.val + 1000)) % 1000000007
        count += 1
        cur = cur.next
    acc[0] = (a * 131 + (count + 1)) % 1000000007


def main() -> None:
    acc = [0]
    report([1, 4, 3, 2, 5, 2], 3, acc)
    report([2, 1], 2, acc)
    report([], 0, acc)
    report([1], 2, acc)
    report([1, 1, 1], 1, acc)
    report([1, 2, 3], 5, acc)
    report([1, 2, 3], 0, acc)
    report([5, 4, 3, 2, 1], 3, acc)
    report([3, 1, 2], 3, acc)
    report([-2, 5, -1, 3, 0, -4], 0, acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
