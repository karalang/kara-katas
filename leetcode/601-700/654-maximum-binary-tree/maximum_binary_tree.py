# LeetCode #654: Maximum Binary Tree -- a stack of the right spine.
# Mirrors the ★ arm (maximum_binary_tree.kara) and its test harness.
import sys
from collections import deque

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def construct_maximum_binary_tree(nums):
    stack = []
    for x in nums:
        node = TreeNode(x)
        while stack and stack[-1].val < x:
            node.left = stack.pop()
        if stack:
            stack[-1].right = node
        stack.append(node)
    return stack[0] if stack else None


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def level_order(root):
    items = []
    queue = deque([root])
    while queue:
        n = queue.popleft()
        if n is None:
            items.append("null")
        else:
            items.append(str(n.val))
            queue.append(n.left)
            queue.append(n.right)
    while items and items[-1] == "null":
        items.pop()
    return "[" + ",".join(items) + "]"


def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def fold(node, h):
    if node is None:
        return (h * 31 + 7) % 1000000007
    return fold(node.right, fold(node.left, (h * 31 + node.val + 11) % 1000000007))


def shuffled(n, rng):
    nums = list(range(n))
    i = n - 1
    while i > 0:
        j = rng.next() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
        i -= 1
    return nums


def show(nums):
    print(f"{len(nums)} numbers -> {level_order(construct_maximum_binary_tree(nums))}")


def main():
    show([3, 2, 1, 6, 0, 5])
    show([3, 2, 1])
    show([7])
    show([1, 2, 3, 4])
    show([1, 3, 5, 4, 2])
    show([2, 9, 1, 8, 3, 7])
    show([0, 1000, 999])
    rng = Rng(654)
    heights = 0
    checksum = 0
    for _ in range(300):
        n = 1 + rng.next() % 50
        root = construct_maximum_binary_tree(shuffled(n, rng))
        heights += height(root)
        checksum = fold(root, checksum)
    print(f"300 random orders: total height {heights}, checksum {checksum}")
    root = construct_maximum_binary_tree(shuffled(1000, rng))
    print(f"1000 shuffled: height {height(root)}, checksum {fold(root, 0)}")
    root = construct_maximum_binary_tree(list(range(1000)))
    print(f"1000 rising: height {height(root)}, checksum {fold(root, 0)}")
    root = construct_maximum_binary_tree([999 - i for i in range(1000)])
    print(f"1000 falling: height {height(root)}, checksum {fold(root, 0)}")


main()
