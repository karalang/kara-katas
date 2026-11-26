# LeetCode #1448 Count Good Nodes in Binary Tree: a mirror of good_nodes.kara.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def good_nodes(root):
    return below(root, -(2**31))


# the good nodes under `node`, `high` the largest value on the path above
# it: the node is good when it is at least as large
def below(node, high):
    if node is None:
        return 0
    good = 1 if node.val >= high else 0
    high = max(high, node.val)
    return good + below(node.left, high) + below(node.right, high)


# ---- test harness ---------------------------------------------------------

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
        if head == len(queue):
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
    root = TreeNode(next_random() % (2 * top + 1) - top)
    places = [(root, True), (root, False)]
    for _ in range(1, n):
        k = next_random() % len(places)
        places[k], places[-1] = places[-1], places[k]
        parent, left = places.pop()
        node = TreeNode(next_random() % (2 * top + 1) - top)
        if left:
            parent.left = node
        else:
            parent.right = node
        places.append((node, True))
        places.append((node, False))
    return root


def chain(n, rising):
    tree = None
    for i in range(n - 1, -1, -1):
        v = i * 2 % 20001 - 10000
        tree = TreeNode(v if rising else -v, None, tree)
    return tree


def main():
    global seed
    e1 = good_nodes(from_level([3, 1, 4, 3, None, 1, 5]))
    e2 = good_nodes(from_level([3, 3, None, 4, 2]))
    e3 = good_nodes(from_level([1]))
    falling = [10000 - i % 20001 for i in range(65535)]
    same = [-7] * 65535
    print(f"{e1} {e2} {e3} {good_nodes(chain(10000, True))} {good_nodes(chain(10000, False))} {good_nodes(from_level(falling))} {good_nodes(from_level(same))}")
    seed = 1448
    print(f"10^5 nodes: {good_nodes(random_tree(100000, 10000))}")
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 300
        top = next_random() % 101
        got = good_nodes(random_tree(n, top))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random trees: {total} good nodes, checksum {check}")


main()
