# Benchmark for #426: mirror of tree_to_list.kara (the in-order
# recursion). The walk breaks every link, as the Kāra program does, so
# reference counting frees the nodes without the cycle collector.
import sys

sys.setrecursionlimit(10000)


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def link(node, state):
    if node is None:
        return
    link(node.left, state)
    last = state[1]
    if last is not None:
        last.right = node
        node.left = last
    else:
        state[0] = node
    state[1] = node
    link(node.right, state)


def tree_to_doubly_list(root):
    state = [None, None]  # first, last
    link(root, state)
    first, last = state
    if first is None:
        return None
    first.left = last
    last.right = first
    return first


seed = 426


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def insert(root, val):
    if root is None:
        return Node(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root


def main():
    n = 50000
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    order = list(range(n))
    checksum = 0
    for _ in range(rounds):
        for i in range(n - 1):
            a = step()
            b = step()
            j = i + (a * 32768 + b) % (n - i)
            order[i], order[j] = order[j], order[i]
        root = None
        for v in order:
            root = insert(root, v)
        head = tree_to_doubly_list(root)
        root = None
        checksum = (checksum * 31 + head.left.val) % 1000000007
        cur = head
        head = None
        for _ in range(n):
            checksum = (checksum * 31 + cur.val) % 1000000007
            nxt = cur.right
            cur.left = None
            cur.right = None
            cur = nxt
    print(f"{rounds} rounds on {n} nodes: checksum {checksum}")


main()
