# LeetCode #1157: Online Majority Element In Subarray -- a Python mirror of
# the ★ arm: a segment tree of Boyer-Moore votes and the sorted places of
# each value. Its output is byte-identical to majority_checker.kara.
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
        while lo < hi:
            if lo % 2 == 1:
                won = vote(won, self.tree[lo])
                lo += 1
            if hi % 2 == 1:
                hi -= 1
                won = vote(won, self.tree[hi])
            lo //= 2
            hi //= 2
        p = self.places[won[0]]
        count = bisect_right(p, right) - bisect_left(p, left)
        return won[0] if count >= threshold else -1


# ---- test harness ---------------------------------------------------------

class Seed:
    def __init__(self, s):
        self.s = s

    def next(self):
        self.s = (self.s * 1103515245 + 12345) % 2147483648
        return self.s // 65536


def array(seed, n, k):
    if k == 0:
        v = 1 + seed.next() % 20000
        out = []
        for _ in range(n):
            out.append(v if seed.next() % 3 < 2 else 1 + seed.next() % 20000)
        return out
    return [1 + seed.next() % k for _ in range(n)]


def session(seed, arr, queries, make=MajorityChecker):
    n = len(arr)
    checker = make(arr)
    total = check = 0
    for _ in range(queries):
        a = seed.next() % n
        b = seed.next() % n
        left, right = min(a, b), max(a, b)
        least = (right - left + 1) // 2 + 1
        threshold = least + seed.next() % (right - left + 2 - least)
        got = checker.query(left, right, threshold)
        total += got
        check = (check * 31 + got + 1) % 1000000007
    return total, check


def main(make=MajorityChecker):
    c = make([1, 1, 2, 2, 1, 1])
    print(f"query(0, 5, 4) = {c.query(0, 5, 4)}, query(0, 3, 3) = {c.query(0, 3, 3)}, query(2, 3, 2) = {c.query(2, 3, 2)}")
    one = make([7])
    print(f"query(0, 0, 1) = {one.query(0, 0, 1)}")
    two = make([1, 2])
    print(f"query(0, 1, 2) = {two.query(0, 1, 2)}, query(1, 1, 1) = {two.query(1, 1, 1)}")
    run = make([5, 5, 5, 5, 5])
    print(f"query(1, 3, 3) = {run.query(1, 3, 3)}, query(0, 4, 5) = {run.query(0, 4, 5)}")
    turn = make([1, 2, 1, 2, 1])
    print(f"query(0, 4, 3) = {turn.query(0, 4, 3)}, query(1, 3, 2) = {turn.query(1, 3, 2)}, query(0, 3, 3) = {turn.query(0, 3, 3)}")
    big = make([20000, 1, 20000])
    print(f"query(0, 2, 2) = {big.query(0, 2, 2)}, query(0, 2, 3) = {big.query(0, 2, 3)}")
    seed = Seed(1157)
    total = check = 0
    for _ in range(300):
        n = 1 + seed.next() % 60
        k = seed.next() % 5
        arr = array(seed, n, k)
        t, c = session(seed, arr, 20, make)
        total += t
        check = (check * 31 + c) % 1000000007
    print(f"300 random arrays: total {total}, checksum {check}")
    for k in [2, 0, 1]:
        arr = array(seed, 20000, k)
        t, c = session(seed, arr, 10000, make)
        print(f"20000 values, 10000 queries: total {t}, checksum {c}")


if __name__ == "__main__":
    main()
