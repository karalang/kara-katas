# LeetCode #366: Find Leaves of Binary Tree -- mirror of find_leaves.kara.
# A tree is None or a tuple (value, left, right).
from collections import deque


def parse_level_order(s):
    body = s[1:-1]
    if not body:
        return []
    return [None if t == "null" else int(t) for t in body.split(",")]


def links(items):
    vals, left, right = [], [], []
    if not items or items[0] is None:
        return vals, left, right
    vals.append(items[0])
    left.append(-1)
    right.append(-1)
    queue = deque([0])
    i = 1
    while i < len(items):
        if not queue:
            break
        parent = queue.popleft()
        for side in range(2):
            if i < len(items):
                if items[i] is not None:
                    node = len(vals)
                    vals.append(items[i])
                    left.append(-1)
                    right.append(-1)
                    if side == 0:
                        left[parent] = node
                    else:
                        right[parent] = node
                    queue.append(node)
                i += 1
    return vals, left, right


def build(l, node):
    vals, left, right = l
    if node < 0:
        return None
    return (vals[node], build(l, left[node]), build(l, right[node]))


def file_by_height(t, out):
    if t is None:
        return -1
    v, left, right = t
    h = 1 + max(file_by_height(left, out), file_by_height(right, out))
    if h == len(out):
        out.append([])
    out[h].append(v)
    return h


def find_leaves(items):
    l = links(items)
    out = []
    if l[0]:
        file_by_height(build(l, 0), out)
    return out


def show(label, text):
    print(f"{label}: {find_leaves(parse_level_order(text))}")


def main():
    show("example 1", "[1,2,3,4,5]")
    show("example 2", "[1]")
    show("an empty tree", "[]")
    show("a left chain", "[1,2,null,3,null,4]")
    show("a right chain", "[1,null,2,null,3]")
    show("a perfect tree", "[1,2,3,4,5,6,7]")
    show("a shallow leaf beside a deep one", "[1,2,3,null,null,4,5,null,6]")
    show("negative and repeated values", "[-1,-1,0,null,-100,100,0]")
    show("a two-node tree", "[5,null,6]")
    seed = 366
    checksum = 0
    groups = 0
    for _ in range(400):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + (seed // 65536) % 40
        items = []
        for k in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            r = seed // 65536
            items.append(None if k > 0 and r % 4 == 0 else r % 201 - 100)
        for group in find_leaves(items):
            groups += 1
            for v in group:
                checksum = (checksum * 31 + v + 101) % 1000000007
            checksum = (checksum * 31 + 7) % 1000000007
    print(f"400 random trees: {groups} groups, checksum {checksum}")


main()
