# LeetCode #971: Flip Binary Tree To Match Preorder Traversal -- Python
# mirror of flip_match_voyage.kara.

from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def walk(t, voyage, i, flipped):
    if t is None:
        return True
    if t.val != voyage[i[0]]:
        return False
    i[0] += 1
    if t.left is not None and t.left.val != voyage[i[0]]:
        flipped.append(t.val)
        return walk(t.right, voyage, i, flipped) and walk(t.left, voyage, i, flipped)
    return walk(t.left, voyage, i, flipped) and walk(t.right, voyage, i, flipped)


def flip_match_voyage(root, voyage):
    flipped = []
    if walk(root, voyage, [0], flipped):
        return flipped
    return [-1]


# ---- test harness -----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(vals):
    if not vals or vals[0] is None:
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


def random_permutation(n):
    a = list(range(1, n + 1))
    i = n - 1
    while i > 0:
        j = next_random() % (i + 1)
        a[i], a[j] = a[j], a[i]
        i -= 1
    return a


def random_tree(vals):
    root = TreeNode(vals[0])
    for k in range(1, len(vals)):
        node = TreeNode(vals[k])
        cur = root
        while True:
            if next_random() % 2 == 0:
                if cur.left is not None:
                    cur = cur.left
                else:
                    cur.left = node
                    break
            else:
                if cur.right is not None:
                    cur = cur.right
                else:
                    cur.right = node
                    break
    return root


def random_voyage(t, out):
    if t is not None:
        out.append(t.val)
        if next_random() % 2 == 0:
            random_voyage(t.left, out)
            random_voyage(t.right, out)
        else:
            random_voyage(t.right, out)
            random_voyage(t.left, out)


def mirrored(t, out):
    if t is not None:
        out.append(t.val)
        mirrored(t.right, out)
        mirrored(t.left, out)


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    global seed
    cases = [
        ([1, 2], [2, 1]),
        ([1, 2, 3], [1, 3, 2]),
        ([1, 2, 3], [1, 2, 3]),
        ([1], [1]),
        ([1, None, 2], [1, 2]),
        ([1, 2, 3, 4, 5, 6, 7], [1, 3, 7, 6, 2, 5, 4]),
        ([1, 2, 3, 4, 5, 6, 7], [1, 3, 6, 7, 2, 4, 5]),
        ([1, 2, 3, 4, 5, 6, 7], [1, 2, 4, 3, 5, 6, 7]),
        ([2, 1, None, 4, 3], [2, 1, 3, 4]),
        ([1, 2, None, 3], [1, 3, 2]),
    ]
    for tree, voyage in cases:
        got = sorted(flip_match_voyage(from_level_order(tree), voyage))
        print(f"voyage {show(voyage)}: {show(got)}")
    seed = 971
    nodes = matched = flips = check = 0
    for c in range(300):
        n = 1 + next_random() % 12
        root = random_tree(random_permutation(n))
        nodes += n
        voyage = []
        random_voyage(root, voyage)
        if c % 4 == 2:
            i = next_random() % n
            j = next_random() % n
            voyage[i], voyage[j] = voyage[j], voyage[i]
        elif c % 4 == 3:
            voyage = random_permutation(n)
        got = sorted(flip_match_voyage(root, voyage))
        if got != [-1]:
            matched += 1
            flips += len(got)
        for v in got:
            check = (check * 31 + v + 2) % 1000000007
        check = (check * 31 + 1) % 1000000007
    print(f"300 random trees of {nodes} nodes: {matched} matched with {flips} flips, checksum {check}")
    root = random_tree(random_permutation(100))
    voyage = []
    random_voyage(root, voyage)
    got = sorted(flip_match_voyage(root, voyage))
    print(f"a random tree of 100 nodes: {len(got)} flips, {show(got)}")
    voyage[98], voyage[99] = voyage[99], voyage[98]
    print(f"the same with its last two swapped: {show(flip_match_voyage(root, voyage))}")
    complete = from_level_order(list(range(1, 101)))
    mirror = []
    mirrored(complete, mirror)
    every = sorted(flip_match_voyage(complete, mirror))
    print(f"the complete tree of 100 nodes read mirrored: {len(every)} flips, the first {every[0]} and the last {every[-1]}")


main()
