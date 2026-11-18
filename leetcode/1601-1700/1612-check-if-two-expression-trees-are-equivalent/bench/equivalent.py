# LeetCode #1612: Check If Two Expression Trees are Equivalent -- the bench
# in Python, mirroring equivalent.kara: one walk counts the first tree's
# leaves up and the second's down, into one list of 26 counts.


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
            counts[ord(node.val) - 97] += sign


def check_equivalence(root1, root2):
    counts = [0] * 26
    tally(root1, 1, counts)
    tally(root2, -1, counts)
    return all(c == 0 for c in counts)


def main():
    seed = 1612

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def big():
        a = next_random()
        return a * 32768 + next_random()

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

    n = 50000
    pairs = []
    for _ in range(10):
        leaves = [chr(97 + next_random() % 26) for _ in range(n)]
        other = list(leaves)
        for i in range(n - 1, 0, -1):
            j = big() % (i + 1)
            other[i], other[j] = other[j], other[i]
        if next_random() % 2 == 0:
            i = big() % n
            other[i] = chr(97 + next_random() % 26)
        one = random_expression(leaves)
        two = random_expression(other)
        pairs.append((one, two))
    check = equivalent = 0
    for one, two in pairs:
        for k in range(10):
            same = check_equivalence(one, two) if k % 2 == 0 else check_equivalence(two, one)
            if same:
                equivalent += 1
            check = (check * 31 + (1 if same else 0) + 1) % 1000000007
    print(f"10 pairs of 50000 leaves from 26 letters, 100 checks: {equivalent} equivalent, checksum {check}")


main()
