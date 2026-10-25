# Benchmark: LeetCode #998 Maximum Binary Tree II -- the ★ arm, down the
# right spine by recursion, on maximum trees of 99 values, LeetCode's
# largest. Mirrors insert_into_max_tree.kara, .c, .rs and go-seq/.


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def insert_into_max_tree(root, val):
    if root is None:
        return TreeNode(val)
    if val > root.val:
        return TreeNode(val, root, None)
    root.right = insert_into_max_tree(root.right, val)
    return root


seed = 998


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(a, lo, hi):
    if lo >= hi:
        return None
    m = lo
    for i in range(lo + 1, hi):
        if a[i] > a[m]:
            m = i
    return TreeNode(a[m], build(a, lo, m), build(a, m + 1, hi))


# Take val out again, from where the insert put it on the right spine,
# and return the tree as it was with how deep val sat.
def take_out(root, val):
    if root.val == val:
        return root.left, 0
    above = root
    depth = 1
    while True:
        nxt = above.right
        if nxt.val == val:
            above.right = nxt.left
            return root, depth
        above = nxt
        depth += 1


def main():
    rounds = 100000
    # 20 trees of the 99 values from 1 to 100 but one: the even ones in a
    # random order, the odd ones falling, which makes a chain of 99
    trees = []
    vals = []
    for t in range(20):
        val = 1 + next_random() % 100
        a = [100 - v for v in range(100) if 100 - v != val]
        if t % 2 == 0:
            i = 98
            while i > 0:
                j = next_random() % (i + 1)
                a[i], a[j] = a[j], a[i]
                i -= 1
        trees.append(build(a, 0, 99))
        vals.append(val)
    depths = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            k = (r + i) % 20
            got = insert_into_max_tree(trees[k], vals[k])
            tree, depth = take_out(got, vals[k])
            trees[k] = tree
            depths += depth
            check = (check * 31 + depth + 1) % 1000000007
    print(f"{rounds} rounds over 20 trees of 99 values: depth total {depths}, checksum {check}")


main()
