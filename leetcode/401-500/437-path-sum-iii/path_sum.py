# LeetCode #437: Path Sum III -- mirror of path_sum.kara (prefix sums
# along the path).


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def count_from(node, prefix, target, seen):
    if node is None:
        return 0
    total = prefix + node.val
    found = seen.get(total - target, 0)
    seen[total] = seen.get(total, 0) + 1
    found += count_from(node.left, total, target, seen)
    found += count_from(node.right, total, target, seen)
    seen[total] -= 1
    return found


def path_sum(root, target):
    return count_from(root, 0, target, {0: 1})


NULL = -1000000007


def build(vals):
    if not vals or vals[0] == NULL:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    head = 0
    i = 1
    while head < len(queue) and i < len(vals):
        cur = queue[head]
        head += 1
        if vals[i] != NULL:
            cur.left = TreeNode(vals[i])
            queue.append(cur.left)
        i += 1
        if i < len(vals) and vals[i] != NULL:
            cur.right = TreeNode(vals[i])
            queue.append(cur.right)
        i += 1
    return root


def show(vals, target):
    text = "[" + ",".join("null" if v == NULL else str(v) for v in vals) + "]"
    print(f"{text}, target {target}: {path_sum(build(vals), target)}")


seed = 437


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([10, 5, -3, 3, 2, NULL, 11, 3, -2, NULL, 1], 8)
    show([5, 4, 8, 11, NULL, 13, 4, 7, 2, NULL, NULL, 5, 1], 22)
    show([], 0)
    show([7], 7)
    show([0, 0, 0, 0], 0)
    show([1, NULL, -1, NULL, 1, NULL, -1, NULL, 1], 0)
    show([1000000000, 1000000000, NULL, 1000000000, NULL, 1000000000], 3000000000)
    show([-1000000000, NULL, -1000000000, NULL, -1000000000], -2000000000)
    show([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 15)
    # 300 random trees of up to 60 nodes with values in [-5, 5], each
    # node given a free slot of the level order with probability 3/4,
    # and a target in [-5, 5].
    total = 0
    checksum = 0
    for _ in range(300):
        n = next_random() % 61
        vals = []
        placed = 0
        while placed < n:
            if vals and next_random() % 4 == 0:
                vals.append(NULL)
            else:
                vals.append(next_random() % 11 - 5)
                placed += 1
        target = next_random() % 11 - 5
        count = path_sum(build(vals), target)
        total += count
        checksum = (checksum * 31 + count) % 1000000007
    print(f"300 random trees: {total} paths, checksum {checksum}")


main()
