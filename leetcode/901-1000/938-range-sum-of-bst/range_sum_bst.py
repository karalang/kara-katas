# LeetCode #938: Range Sum of BST -- recursion that skips subtrees
# (Python mirror).
import sys
from collections import deque

sys.setrecursionlimit(100000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def range_sum_bst(root, low, high):
    if root is None:
        return 0
    if root.val < low:
        return range_sum_bst(root.right, low, high)
    if root.val > high:
        return range_sum_bst(root.left, low, high)
    return root.val + range_sum_bst(root.left, low, high) + range_sum_bst(root.right, low, high)


# ---- test harness ---------------------------------------------------------

seed = 938


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(vals):
    if len(vals) == 0 or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while i < len(vals):
        node = queue.popleft()
        if vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals):
            if vals[i] is not None:
                node.right = TreeNode(vals[i])
                queue.append(node.right)
            i += 1
    return root


def insert_all(vals):
    root = TreeNode(vals[0])
    for v in vals[1:]:
        cur = root
        while True:
            if v == cur.val:
                break
            if v < cur.val:
                if cur.left is None:
                    cur.left = TreeNode(v)
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = TreeNode(v)
                    break
                cur = cur.right
    return root


def chain(n, rightward):
    top = TreeNode(n if rightward else 1)
    for k in range(1, n):
        node = TreeNode(n - k if rightward else 1 + k)
        if rightward:
            node.right = top
        else:
            node.left = top
        top = node
    return top


def balanced(lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    return TreeNode(mid, balanced(lo, mid - 1), balanced(mid + 1, hi))


def main():
    first = [10, 5, 15, 3, 7, None, 18]
    second = [10, 5, 15, 3, 7, 13, 18, 1, None, 6]
    print(f"[10,5,15,3,7,null,18], 7 to 15: {range_sum_bst(from_level_order(first), 7, 15)}")
    print(f"[10,5,15,3,7,13,18,1,null,6], 6 to 10: {range_sum_bst(from_level_order(second), 6, 10)}")
    print(f"[5], 5 to 5: {range_sum_bst(from_level_order([5]), 5, 5)}")
    print(f"[5], 6 to 9: {range_sum_bst(from_level_order([5]), 6, 9)}")
    print(f"[10,5,15,3,7,null,18], 1 to 100000: {range_sum_bst(from_level_order(first), 1, 100000)}")
    print(f"[10,5,15,3,7,null,18], 11 to 14: {range_sum_bst(from_level_order(first), 11, 14)}")
    print(f"[10,5,15,3,7,13,18,1,null,6], 1 to 1: {range_sum_bst(from_level_order(second), 1, 1)}")
    nodes = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 200
        vals = [1 + next_random() % 100000 for _ in range(n)]
        a = 1 + next_random() % 100000
        b = 1 + next_random() % 100000
        low, high = min(a, b), max(a, b)
        s = range_sum_bst(insert_all(vals), low, high)
        nodes += n
        total += s
        check = (check * 1000003 + s) % 1000000007
    print(f"300 random trees of {nodes} values: sums adding to {total}, checksum {check}")
    pool = list(range(1, 100001))
    for i in range(20000):
        j = i + next_random() % (100000 - i)
        pool[i], pool[j] = pool[j], pool[i]
    vals = pool[:20000]
    print(f"20000 values put in at random, 25000 to 75000: {range_sum_bst(insert_all(vals), 25000, 75000)}")
    print(f"a chain of 20000 to the right, 5000 to 15000: {range_sum_bst(chain(20000, True), 5000, 15000)}")
    print(f"a chain of 20000 to the left, 1 to 20000: {range_sum_bst(chain(20000, False), 1, 20000)}")
    print(f"a balanced tree of 20000, 9999 to 10001: {range_sum_bst(balanced(1, 20000), 9999, 10001)}")


main()
