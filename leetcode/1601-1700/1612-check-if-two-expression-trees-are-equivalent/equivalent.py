# LeetCode #1612: Check If Two Expression Trees are Equivalent -- the
# Python mirror of equivalent.kara: one walk counts the first tree's
# leaves up and the second's down, and the trees are equivalent when every
# count ends at zero.
from collections import deque


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def tally(node, sign, counts):
    if node is not None:
        if node.val == "+":
            tally(node.left, sign, counts)
            tally(node.right, sign, counts)
        else:
            counts[ord(node.val) - ord("a")] += sign


def check_equivalence(root1, root2):
    counts = [0] * 26
    tally(root1, 1, counts)
    tally(root2, -1, counts)
    return all(c == 0 for c in counts)


def from_level_order(items):
    root = Node(items[0])
    queue = deque([root])
    i = 1
    while i < len(items):
        node = queue.popleft()
        for side in range(2):
            if i < len(items):
                if items[i] is not None:
                    child = Node(items[i])
                    if side == 0:
                        node.left = child
                    else:
                        node.right = child
                    queue.append(child)
                i += 1
    return root


seed = 1612


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big():
    a = next_random()
    return a * 32768 + next_random()


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def swap_remove(v, i):
    v[i], v[-1] = v[-1], v[i]
    return v.pop()


def random_expression(leaves):
    loose = [Node(c) for c in leaves]
    while len(loose) > 1:
        a = swap_remove(loose, big() % len(loose))
        b = swap_remove(loose, big() % len(loose))
        loose.append(Node("+", a, b))
    return loose[0]


def batch(count, most, letters):
    check = seen = equivalent = 0
    for _ in range(count):
        n = big() % most + 1
        leaves = [chr(ord("a") + next_random() % letters) for _ in range(n)]
        other = list(leaves)
        for i in range(n - 1, 0, -1):
            j = big() % (i + 1)
            other[i], other[j] = other[j], other[i]
        if next_random() % 2 == 0:
            i = big() % n
            other[i] = chr(ord("a") + next_random() % letters)
        first = random_expression(leaves)
        second = random_expression(other)
        same = check_equivalence(first, second)
        if same:
            equivalent += 1
        check = mix(check, 1 if same else 0)
        seen += n
    print(f"{count} pairs of up to {most} leaves from {letters} letters: {seen} leaves, {equivalent} equivalent, checksum {check}")


examples = [
    (["x"], ["x"]),
    (["+", "a", "+", None, None, "b", "c"], ["+", "+", "a", "b", "c"]),
    (["+", "a", "+", None, None, "b", "c"], ["+", "+", "a", "b", "d"]),
    (["a"], ["+", "a", "a"]),
    (["+", "a", "a"], ["+", "a", "b"]),
    (["+", "+", "+", "a", "b", "c", "d"], ["+", "d", "+", None, None, "c", "+", None, None, "b", "a"]),
]
for one, two in examples:
    print("true" if check_equivalence(from_level_order(one), from_level_order(two)) else "false")
batch(3000, 6, 3)
batch(300, 1000, 26)
batch(3, 100000, 26)
