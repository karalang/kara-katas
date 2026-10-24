# LeetCode #938: Range Sum of BST -- bench: recursion that skips
# subtrees. Mirrors range_sum_bst.kara, .c, .rs and go-seq/.


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


seed = 938


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 20
    count = 20
    queries = 50
    trees = []
    lows = []
    highs = []
    pool = list(range(1, 100001))
    for _ in range(count):
        for i in range(20000):
            j = i + next_random() % (100000 - i)
            pool[i], pool[j] = pool[j], pool[i]
        root = TreeNode(pool[0])
        for v in pool[1:20000]:
            cur = root
            while True:
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
        trees.append(root)
        for _ in range(queries):
            a = 1 + next_random() % 100000
            b = 1 + next_random() % 100000
            lows.append(min(a, b))
            highs.append(max(a, b))
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            c = (r + i) % count
            for q in range(queries):
                s = range_sum_bst(trees[c], lows[c * queries + q], highs[c * queries + q])
                total += s
                check = (check * 1000003 + s) % 1000000007
    print(f"{rounds} rounds over {count} trees of 20000 nodes, {queries} ranges each: sums adding to {total}, checksum {check}")


main()
