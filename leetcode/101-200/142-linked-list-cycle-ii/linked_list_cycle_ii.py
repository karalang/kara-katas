"""LeetCode 142 — Linked List Cycle II (Python mirror / oracle).

Floyd's two-phase: phase 1 finds a meeting point in the cycle; phase 2 resets
one pointer to the head and advances both one step at a time until they meet at
the cycle entry. Returns the entry node's id, or -1 for an acyclic list. The
Kāra version uses a Vec-owned + `weak` next overlay so a cycle is leak-free.
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


def detect_cycle(head):
    slow = fast = head
    met = False
    while True:
        if fast is None or fast.next is None:
            return -1
        fast = fast.next.next
        if slow is None:
            return -1
        slow = slow.next
        if slow is not None and fast is not None and slow.id == fast.id:
            met = True
            break
    if not met:
        return -1
    slow = head
    while True:
        if slow is None or fast is None:
            return -1
        if slow.id == fast.id:
            return slow.id
        slow = slow.next
        fast = fast.next


def run(vals, nxt):
    nodes = build(vals, nxt)
    head = nodes[0] if len(vals) > 0 else None
    print(detect_cycle(head))


def main():
    run([3, 2, 0, -4], [1, 2, 3, 1])
    run([1, 2], [1, 0])
    run([1], [-1])
    run([1, 2, 3, 4, 5], [1, 2, 3, 4, -1])


main()
