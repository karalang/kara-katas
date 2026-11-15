# LeetCode #1157 bench: the ★ arm's vote tree and sorted places, the same
# workload as majority_checker.kara.
from bisect import bisect_left, bisect_right


def vote(a, b):
    if a[0] == b[0]:
        return (a[0], a[1] + b[1])
    if a[1] >= b[1]:
        return (a[0], a[1] - b[1])
    return (b[0], b[1] - a[1])


class MajorityChecker:
    def __init__(self, arr):
        n = len(arr)
        size = 1
        while size < n:
            size *= 2
        tree = [(0, 0)] * (2 * size)
        places = [[] for _ in range(20001)]
        for i, x in enumerate(arr):
            tree[size + i] = (x, 1)
            places[x].append(i)
        for i in range(size - 1, 0, -1):
            tree[i] = vote(tree[2 * i], tree[2 * i + 1])
        self.size, self.tree, self.places = size, tree, places

    def query(self, left, right, threshold):
        lo, hi = left + self.size, right + self.size + 1
        won = (0, 0)
        tree = self.tree
        while lo < hi:
            if lo % 2 == 1:
                won = vote(won, tree[lo])
                lo += 1
            if hi % 2 == 1:
                hi -= 1
                won = vote(won, tree[hi])
            lo //= 2
            hi //= 2
        p = self.places[won[0]]
        count = bisect_right(p, right) - bisect_left(p, left)
        return won[0] if count >= threshold else -1


def main():
    passes = 100
    s = 1157

    def rnd():
        nonlocal s
        s = (s * 1103515245 + 12345) % 2147483648
        return s // 65536
    checkers, queries = [], []
    for kind in range(4):
        v = 1 + rnd() % 20000
        arr = []
        for _ in range(20000):
            if kind == 0:
                x = 1 + rnd() % 2
            elif kind == 2:
                x = 1 + rnd() % 20000
            elif rnd() % 100 < (67 if kind == 1 else 50):
                x = v
            else:
                x = 1 + rnd() % 20000
            arr.append(x)
        checkers.append(MajorityChecker(arr))
        qs = []
        for _ in range(10000):
            a = rnd() % 20000
            b = rnd() % 20000
            left, right = min(a, b), max(a, b)
            least = (right - left + 1) // 2 + 1
            qs.append((left, right, least + rnd() % (right - left + 2 - least)))
        queries.append(qs)
    check = 0
    for p in range(passes):
        for k in range(4):
            c = checkers[k]
            for (left, right, threshold) in queries[k]:
                check = (check * 31 + c.query(left, right, threshold) + p + 1) % 1000000007
    print(f"{passes} passes over 4 arrays of 20000 values, 10000 queries each: checksum {check}")


main()
