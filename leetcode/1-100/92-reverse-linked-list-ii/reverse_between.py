"""LeetCode #92: Reverse Linked List II — one-pass head insertion.

Mirror of reverse_between.kara. A dummy before the head; walk `prev` to just before
position `left`, then repeatedly head-insert the node after `cur` in front of `prev`
(right - left) times, reversing the section while `cur` drifts to its tail. Same nine
cases and output shape (a `[left,right]: [...]` line per case, then a `sink:` fold of
length + values) so the files diff line-for-line.
"""

from __future__ import annotations

from typing import Optional


class ListNode:
    def __init__(self, val: int, nxt: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = nxt


def reverse_between(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(1, left):
        prev = prev.next
    cur = prev.next
    for _ in range(left, right):
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt
    return dummy.next


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


def report(arr: list[int], left: int, right: int, acc: list[int]) -> None:
    out = reverse_between(from_array(arr), left, right)
    print(f"[{left},{right}]: {to_string(out)}")
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
    report([1, 2, 3, 4, 5], 2, 4, acc)
    report([5], 1, 1, acc)
    report([1, 2, 3], 1, 3, acc)
    report([1, 2, 3, 4, 5], 1, 5, acc)
    report([1, 2, 3, 4, 5], 2, 2, acc)
    report([3, 5], 1, 2, acc)
    report([1, 2, 3, 4, 5, 6, 7], 3, 6, acc)
    report([1, 2, 3, 4], 2, 4, acc)
    report([-1, -3, 2, 5], 1, 4, acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
