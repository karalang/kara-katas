"""LeetCode 237 — Delete Node in a Linked List (Python mirror / oracle).

Index-pool singly-linked list (list of nodes, i64 next, -1 = null). Given only
the node, copy the successor's value into it and splice the successor out — the
node you were handed always survives; the one that leaves is `node.next`.
Mirrors the Kāra version; the shift-down variant prints the same values.
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


def delete_node(nodes, node):
    succ = nodes[node].next
    nodes[node].val = nodes[succ].val
    nodes[node].next = nodes[succ].next


def show(nodes, head):
    out = []
    cur = head
    while cur != -1:
        out.append(str(nodes[cur].val))
        cur = nodes[cur].next
    print(" ".join(out))


def report(vals, node):
    nodes = build(vals)
    delete_node(nodes, node)
    show(nodes, 0)


def main():
    report([4, 5, 1, 9], 1)
    report([4, 5, 1, 9], 2)
    report([1, 2], 0)
    report([0, 1, 2, 3, 4, 5, 6, 7], 6)
    report([7, 7, 7, 7], 2)
    report([1, 2, 3], 0)
    report([1, 2, 3], 1)


main()
