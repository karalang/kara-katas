"""LeetCode #82: Remove Duplicates from Sorted List II — iterative, dummy + prev.

Mirror of remove_duplicates_ii_list.kara. A dummy sits before the head; a `prev`
cursor tracks the last node known to be kept, a `cur` cursor scans forward. When cur
and its successor share a value, cur starts a duplicate run — advance a runner past
every node equal to cur.val, then splice the whole run out with prev.next = runner
(prev does NOT move). Otherwise keep cur and advance prev. Same ten cases and output
shape (a rendered `[...]` list per case, then a `sink:` fold of length + survivors)
so the files diff line-for-line.
"""

from __future__ import annotations

from typing import Optional


class ListNode:
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


def report(arr: list[int], acc: list[int]) -> None:
    out = delete_duplicates(from_array(arr))
    print(to_string(out))
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
    report([1, 2, 3, 3, 4, 4, 5], acc)
    report([1, 1, 1, 2, 3], acc)
    report([1, 1], acc)
    report([1, 2, 3], acc)
    report([], acc)
    report([1], acc)
    report([1, 1, 2, 2, 3, 3], acc)
    report([1, 2, 2], acc)
    report([-1, -1, 0, 1], acc)
    report([1, 1, 2, 3, 3, 4], acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
