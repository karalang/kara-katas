"""LeetCode 141 — Linked List Cycle (Python mirror / oracle).

Floyd's tortoise-and-hare over a `next` overlay. The Kāra version models nodes
as Vec-owned with a `weak` next link (so a cycle is leak-free under reference
counting); Python is GC'd, so the mirror uses ordinary references.
"""


class Node:
    def __init__(self, val, id):
        self.val = val
        self.id = id
        self.next = None


def build(vals, nxt):
    nodes = [Node(vals[i], i) for i in range(len(vals))]
    for i in range(len(vals)):
        if nxt[i] >= 0:
            nodes[i].next = nodes[nxt[i]]
    return nodes


def has_cycle(head):
    slow = head
    fast = head
    while True:
        if fast is None or fast.next is None:
            return False
        fast = fast.next.next
        if slow is None:
            return False
        slow = slow.next
        if slow is not None and fast is not None and slow.id == fast.id:
            return True


def run(vals, nxt):
    nodes = build(vals, nxt)
    head = nodes[0] if len(vals) > 0 else None
    print("true" if has_cycle(head) else "false")


def main():
    run([3, 2, 0, -4], [1, 2, 3, 1])
    run([1, 2], [1, 0])
    run([1], [-1])
    run([1, 2, 3, 4, 5], [1, 2, 3, 4, -1])


main()
