# LeetCode #1457 Pseudo-Palindromic Paths in a Binary Tree: a mirror of
# pseudo_palindromic_paths.kara.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def pseudo_palindromic_paths(root):
    return paths(root, 0)


# the pseudo-palindromic paths through `node`, `seen` with bit v set when
# the value v is on the path above it an odd number of times: at a leaf
# the path can be rearranged into a palindrome when at most one bit is set
def paths(node, seen):
    if node is None:
        return 0
    seen ^= 1 << node.val
    if node.left is None and node.right is None:
        return 1 if seen & (seen - 1) == 0 else 0
    return paths(node.left, seen) + paths(node.right, seen)


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
    root = TreeNode(1 + next_random() % top)
    places = [(root, True), (root, False)]
    for _ in range(1, n):
        k = next_random() % len(places)
        places[k], places[-1] = places[-1], places[k]
        parent, left = places.pop()
        node = TreeNode(1 + next_random() % top)
        if left:
            parent.left = node
        else:
            parent.right = node
        places.append((node, True))
        places.append((node, False))
    return root


def chain(n, step):
    tree = None
    for i in range(n - 1, -1, -1):
        tree = TreeNode(i * step % 9 + 1, tree, None)
    return tree


def main():
    global seed
    f = pseudo_palindromic_paths
    e1 = f(from_level([2, 3, 1, 3, 1, None, 1]))
    e2 = f(from_level([2, 1, 1, 1, 3, None, None, None, None, None, 1]))
    e3 = f(from_level([9]))
    cycling = [i % 9 + 1 for i in range(65535)]
    same = [4] * 65535
    print(f"{e1} {e2} {e3} {f(chain(10000, 0))} {f(chain(10000, 1))} {f(from_level(cycling))} {f(from_level(same))}")
    seed = 1457
    print(f"10^5 nodes: {f(random_tree(100000, 9))}")
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 300
        top = 1 + next_random() % 9
        got = f(random_tree(n, top))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random trees: {total} paths, checksum {check}")


main()
