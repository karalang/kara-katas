"""LeetCode 234 — Palindrome Linked List (Python mirror / oracle).

O(1)-space: slow/fast to the midpoint, reverse the second half in place, compare
the halves. Index-pool list (list of nodes, i64 next, -1 = null). Mirrors the
Kara version.
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


def reverse(nodes, head):
    prev = -1
    cur = head
    while cur != -1:
        nxt = nodes[cur].next
        nodes[cur].next = prev
        prev = cur
        cur = nxt
    return prev


def is_palindrome(nodes, head):
    if head == -1:
        return True
    slow = head
    fast = head
    while nodes[fast].next != -1 and nodes[nodes[fast].next].next != -1:
        slow = nodes[slow].next
        fast = nodes[nodes[fast].next].next
    second = reverse(nodes, nodes[slow].next)
    p1 = head
    p2 = second
    while p2 != -1:
        if nodes[p1].val != nodes[p2].val:
            return False
        p1 = nodes[p1].next
        p2 = nodes[p2].next
    return True


def report(vals):
    nodes = build(vals)
    head = 0 if nodes else -1
    print("true" if is_palindrome(nodes, head) else "false")


def main():
    report([1, 2, 2, 1])
    report([1, 2])
    report([1])
    report([])
    report([1, 2, 3, 2, 1])
    report([1, 2, 3, 4, 5])
    report([1, 0, 1])
    report([1, 2, 2, 3])
    report([7, 7, 7, 7, 7, 7])


main()
