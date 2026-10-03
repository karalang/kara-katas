# Benchmark workload for LeetCode #333 — Python mirror of largest_bst.kara.
import sys

sys.setrecursionlimit(100000)

NODES = 100000
PUNCHES = 200
MODULUS = 1073741789


def visit(vals, lefts, rights, node, best):
    val = vals[node]
    left = lefts[node]
    right = rights[node]
    bst, size, lo, hi = True, 1, val, val
    if left != -1:
        lb, ls, llo, lhi = visit(vals, lefts, rights, left, best)
        if lb and lhi < val:
            size += ls
            lo = llo
        else:
            bst = False
    if right != -1:
        rb, rs, rlo, rhi = visit(vals, lefts, rights, right, best)
        if rb and rlo > val:
            size += rs
            hi = rhi
        else:
            bst = False
    if bst and size > best[0]:
        best[0] = size
    return bst, size, lo, hi


def largest_bst_subtree(vals, lefts, rights):
    if not vals:
        return 0
    best = [0]
    visit(vals, lefts, rights, 0, best)
    return best[0]


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
    rng = Rng(333)
    order = [i * 2 for i in range(NODES)]
    for i in range(NODES):
        j = i + rng.wide() % (NODES - i)
        order[i], order[j] = order[j], order[i]
    vals, lefts, rights = [], [], []
    for v in order:
        vals.append(v)
        lefts.append(-1)
        rights.append(-1)
        nid = len(vals) - 1
        cur = 0
        while cur != nid:
            if v < vals[cur]:
                if lefts[cur] == -1:
                    lefts[cur] = nid
                cur = lefts[cur]
            else:
                if rights[cur] == -1:
                    rights[cur] = nid
                cur = rights[cur]
    sink = 0
    for _ in range(PUNCHES):
        at = rng.wide() % NODES
        old = vals[at]
        vals[at] = rng.wide() % (2 * NODES)
        answer = largest_bst_subtree(vals, lefts, rights)
        vals[at] = old
        sink = (sink * 1000003 + answer) % MODULUS
    print(sink)


main()
