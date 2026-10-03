# Benchmark workload for LeetCode #337 — Python mirror of house_robber_iii.kara.
import sys

sys.setrecursionlimit(100000)

HOUSES = 500000
PUNCHES = 100
MODULUS = 1073741789


def visit(val, left, right, node):
    if node == -1:
        return (0, 0)
    lr, ls = visit(val, left, right, left[node])
    rr, rs = visit(val, left, right, right[node])
    return (val[node] + ls + rs, max(lr, ls) + max(rr, rs))


def rob(val, left, right):
    if not val:
        return 0
    r, s = visit(val, left, right, 0)
    return max(r, s)


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def wide(self):
        hi = self.next()
        return hi * 32768 + self.next()


def main():
    rng = Rng(337)
    val, left, right = [], [], []
    for i in range(HOUSES):
        val.append(rng.next() % 10001)
        left.append(-1)
        right.append(-1)
        if i == 0:
            continue
        cur = 0
        while True:
            if rng.next() % 2 == 0:
                if left[cur] == -1:
                    left[cur] = i
                    break
                cur = left[cur]
            else:
                if right[cur] == -1:
                    right[cur] = i
                    break
                cur = right[cur]
    sink = 0
    for _ in range(PUNCHES):
        at = rng.wide() % HOUSES
        old = val[at]
        val[at] = rng.next() % 10001
        answer = rob(val, left, right)
        val[at] = old
        sink = (sink * 1000003 + answer) % MODULUS
    print(sink)


main()
