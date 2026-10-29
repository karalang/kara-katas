# LeetCode #1008: Construct Binary Search Tree from Preorder Traversal --
# recursion with an upper bound
#
# Mirrors bst_from_preorder.kara, the ★ arm, and its test harness; its
# output is byte-identical.
from collections import deque


class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def bst_from_preorder(preorder):
    nxt = [0]

    def build(bound):
        if nxt[0] == len(preorder) or preorder[nxt[0]] >= bound:
            return None
        val = preorder[nxt[0]]
        nxt[0] += 1
        left = build(val)
        right = build(bound)
        return TreeNode(val, left, right)

    return build(2**63 - 1)


def serialize(root):
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is not None:
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append("null")
    while out and out[-1] == "null":
        out.pop()
    return "[" + ",".join(out) + "]"


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_preorder(n, most, seed):
    seen = [False] * (most + 1)
    vals = []
    left = []
    right = []
    while len(vals) < n:
        v = 1 + next_random(seed) % most
        if seen[v]:
            continue
        seen[v] = True
        vals.append(v)
        left.append(-1)
        right.append(-1)
        me = len(vals) - 1
        if me > 0:
            at = 0
            while True:
                if v < vals[at]:
                    if left[at] == -1:
                        left[at] = me
                        break
                    at = left[at]
                else:
                    if right[at] == -1:
                        right[at] = me
                        break
                    at = right[at]
    out = []
    stack = [0]
    while stack:
        at = stack.pop()
        out.append(vals[at])
        if right[at] != -1:
            stack.append(right[at])
        if left[at] != -1:
            stack.append(left[at])
    return out


def show(nums):
    return "[" + ",".join(str(x) for x in nums) + "]"


def text_hash(s):
    h = 0
    for c in s:
        h = (h * 131 + ord(c)) % 1000000007
    return h


def main():
    examples = [
        [8, 5, 1, 7, 10, 12],
        [1, 3],
        [1],
        [3, 2, 1],
        [1, 2, 3],
        [4, 2, 1, 3, 6, 5, 7],
        [10, 5, 7, 6, 8, 20, 15],
        [5, 1, 4, 2, 3],
        [2, 1, 9, 3, 8, 4, 7],
    ]
    for preorder in examples:
        print(f"preorder = {show(preorder)} -> {serialize(bst_from_preorder(preorder))}")
    rising = [10 * i + 1 for i in range(100)]
    falling = [1000 - 10 * i for i in range(100)]
    zigzag = [1000 - i // 2 if i % 2 == 0 else 1 + i // 2 for i in range(100)]
    for name, preorder in [("100 rising", rising), ("100 falling", falling), ("100 alternating high and low", zigzag)]:
        text = serialize(bst_from_preorder(preorder))
        print(f"{name} -> {len(text)} characters, hash {text_hash(text)}")
    seed = [1008]
    for count, most, top in [(2000, 8, 20), (500, 100, 1000), (5, 100, 100)]:
        total = 0
        chars = 0
        check = 0
        for _ in range(count):
            size = 1 + next_random(seed) % most
            preorder = random_preorder(size, top, seed)
            text = serialize(bst_from_preorder(preorder))
            total += size
            chars += len(text)
            check = (check * 31 + text_hash(text)) % 1000000007
        print(f"{count} random trees of {total} values: {chars} characters, checksum {check}")


main()
