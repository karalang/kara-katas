# LeetCode #1339: Maximum Product of Splitted Binary Tree -- Python mirror
# of the ★ arm: every subtree's sum s, and the best s * (total - s), taken
# modulo 10^9 + 7 at the end. The walk is iterative here, since Python's
# recursion would not reach the chain's depth.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_product(root):
    order = []
    stack = [root]
    while stack:
        n = stack.pop()
        order.append(n)
        if n.left:
            stack.append(n.left)
        if n.right:
            stack.append(n.right)
    sub = {}
    for n in reversed(order):
        sub[id(n)] = n.val + (sub[id(n.left)] if n.left else 0) + (sub[id(n.right)] if n.right else 0)
    total = sub[id(root)]
    best = max(s * (total - s) for s in sub.values())
    return best % 1000000007


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(values):
        if head >= len(queue):
            break
        node = queue[head]
        head += 1
        if values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


def random_tree(n, top):
    root = TreeNode(1 + next_random() % top)
    places = [(root, True), (root, False)]
    for _ in range(1, n):
        k = next_random() % len(places)
        parent, left = places[k]
        places[k] = places[-1]
        places.pop()
        node = TreeNode(1 + next_random() % top)
        if left:
            parent.left = node
        else:
            parent.right = node
        places.append((node, True))
        places.append((node, False))
    return root


def main():
    global seed
    e1 = max_product(from_level([1, 2, 3, 4, 5, 6]))
    e2 = max_product(from_level([1, None, 2, 3, 4, None, None, 5, 6]))
    two = max_product(from_level([1, 2]))
    chain = None
    for v in range(50000):
        chain = TreeNode(v * 7 % 10000 + 1, None, chain)
    full = [i * 13 % 10000 + 1 for i in range(32767)]
    print(f"{e1} {e2} {two} {max_product(chain)} {max_product(from_level(full))}")
    seed = 1339
    check = 0
    for t in range(1000):
        n = 2 + next_random() % 1999 if t % 20 == 0 else 2 + next_random() % 30
        top = 100 if t % 2 == 0 else 10000
        check = (check * 131 + max_product(random_tree(n, top))) % 1000000007
    print(f"1000 random trees: checksum {check}")


main()
