"""LeetCode 203 — Remove Linked List Elements (Python mirror / oracle).

Index-pool singly-linked list (list of nodes, i64 next, -1 = null): drop leading
matches, then splice prev.next past interior matches. Mirrors the Kāra version.
"""


class Node:
    def __init__(self, val, nxt):
        self.val = val
        self.next = nxt


def build(vals):
    nodes = []
    n = len(vals)
    for i in range(n):
        nodes.append(Node(vals[i], i + 1 if i + 1 < n else -1))
    return nodes


def remove_elements(nodes, head, val):
    new_head = head
    while new_head != -1 and nodes[new_head].val == val:
        new_head = nodes[new_head].next
    if new_head == -1:
        return -1
    prev = new_head
    cur = nodes[new_head].next
    while cur != -1:
        if nodes[cur].val == val:
            nodes[prev].next = nodes[cur].next
        else:
            prev = cur
        cur = nodes[cur].next
    return new_head


def show(nodes, head):
    out = []
    cur = head
    while cur != -1:
        out.append(str(nodes[cur].val))
        cur = nodes[cur].next
    print(" ".join(out))


def report(vals, val):
    nodes = build(vals)
    head = 0 if nodes else -1
    show(nodes, remove_elements(nodes, head, val))


def main():
    report([1, 2, 6, 3, 4, 5, 6], 6)
    report([], 1)
    report([7, 7, 7, 7, 7, 7], 7)
    report([1, 2, 3, 4], 9)
    report([7, 7, 1, 7, 2], 7)


main()
