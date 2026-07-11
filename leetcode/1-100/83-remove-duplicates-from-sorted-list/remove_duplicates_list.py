"""LeetCode #83: Remove Duplicates from Sorted List — iterative, in-place skip.

Mirror of remove_duplicates_list.kara. A single cursor walks the list; when the
current node and its successor share a value, splice the successor out (node.next =
node.next.next) and STAY on the current node so runs of three or more collapse.
Otherwise advance. The head is never deleted (first copy kept), so no dummy. Same ten
cases and output shape (a rendered `[...]` list per case, then a `sink:` fold of
length + survivors) so the files diff line-for-line.
"""

from __future__ import annotations

from typing import Optional


class ListNode:
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
    report([1, 1, 2], acc)
    report([1, 1, 2, 3, 3], acc)
    report([1, 1, 1], acc)
    report([1, 2, 3], acc)
    report([], acc)
    report([7], acc)
    report([1, 1, 2, 2, 3, 3], acc)
    report([1, 2, 2], acc)
    report([-2, -2, -2, 0, 1], acc)
    report([5, 5, 5, 5], acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
