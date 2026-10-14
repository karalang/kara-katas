# LeetCode #617: Merge Two Binary Trees -- Python mirror of the ★ arm
# (recursion, a new tree); see merge_trees.kara.


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def merge_trees(root1, root2):
    if root1 is not None and root2 is not None:
        return TreeNode(root1.val + root2.val,
                        merge_trees(root1.left, root2.left),
                        merge_trees(root1.right, root2.right))
    return root1 if root1 is not None else root2


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def from_level(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(values):
        n = queue[head]
        head += 1
        if values[i] is not None:
            n.left = TreeNode(values[i])
            queue.append(n.left)
        i += 1
        if i < len(values):
            if values[i] is not None:
                n.right = TreeNode(values[i])
                queue.append(n.right)
            i += 1
    return root


def to_level(root):
    parts = []
    queue = [root]
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        if node is not None:
            parts.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            parts.append("null")
    while parts and parts[-1] == "null":
        parts.pop()
    return "[" + ",".join(parts) + "]"


def random_tree(size, lean, seed):
    if size == 0:
        return None
    root = TreeNode(next_random(seed) % 20001 - 10000)
    for _ in range(1, size):
        c = TreeNode(next_random(seed) % 20001 - 10000)
        node = root
        while True:
            if next_random(seed) % 100 < lean:
                if node.left is not None:
                    node = node.left
                else:
                    node.left = c
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = c
                    break
    return root


def show(first, second):
    a = to_level(from_level(first))
    b = to_level(from_level(second))
    print(f"{a} + {b} -> {to_level(merge_trees(from_level(first), from_level(second)))}")


def summary(s):
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) % 1000000007
    return f"{len(s)} characters, checksum {h}"


def main():
    show([1, 3, 2, 5], [2, 1, 3, None, 4, None, 7])
    show([1], [1, 2])
    show([], [])
    show([], [4, 5])
    show([4, None, 6], [])
    show([1, 2], [10, None, 20])
    show([1, 2, None, 3, None, 4], [1, None, 2, None, 3, None, 4])
    show([5, -3, 7], [-5, 3, -7, 1])
    seed = [617]
    total = []
    for _ in range(300):
        leans = [20, 50, 80]
        size = next_random(seed) % 41
        first = random_tree(size, leans[next_random(seed) % 3], seed)
        size = next_random(seed) % 41
        second = random_tree(size, leans[next_random(seed) % 3], seed)
        total.append(to_level(merge_trees(first, second)))
    print(f"300 random pairs: {summary(''.join(total))}")
    first = random_tree(2000, 70, seed)
    second = random_tree(2000, 30, seed)
    print(f"2000 + 2000 nodes: {summary(to_level(merge_trees(first, second)))}")


main()
