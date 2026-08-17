"""Benchmark harness for LeetCode #235 — Lowest Common Ancestor of a BST.

Mirrors lca_bst.kara algorithm-for-algorithm, including the index-pool tree
(parallel lists with -1 = null) rather than linked objects. Committed as the
correctness oracle; not a measured lane.
"""

N = 200000
ITERS = 8000000


def lca(val, left, right, root, p, q):
    cur = root
    while cur != -1:
        v = val[cur]
        if p < v and q < v:
            cur = left[cur]
        elif p > v and q > v:
            cur = right[cur]
        else:
            return v
    return -1


def main():
    vals = []
    x = 7
    for _ in range(N):
        x = (x * 1103515245 + 12345) % 2147483648
        hi = x // 65536
        x = (x * 1103515245 + 12345) % 2147483648
        vals.append((hi * 32768 + x // 65536) % 1000000)

    val = []
    left = []
    right = []
    root = -1
    for b in range(N):
        v = vals[b]
        if root == -1:
            val.append(v)
            left.append(-1)
            right.append(-1)
            root = 0
        else:
            cur = root
            while True:
                if v < val[cur]:
                    l = left[cur]
                    if l == -1:
                        idx = len(val)
                        val.append(v)
                        left.append(-1)
                        right.append(-1)
                        left[cur] = idx
                        break
                    cur = l
                else:
                    r = right[cur]
                    if r == -1:
                        idx = len(val)
                        val.append(v)
                        left.append(-1)
                        right.append(-1)
                        right[cur] = idx
                        break
                    cur = r

    sink = 0
    y = 99
    for _ in range(ITERS):
        y = (y * 1103515245 + 12345) % 2147483648
        phi = y // 65536
        y = (y * 1103515245 + 12345) % 2147483648
        pi = (phi * 32768 + y // 65536) % N
        y = (y * 1103515245 + 12345) % 2147483648
        qhi = y // 65536
        y = (y * 1103515245 + 12345) % 2147483648
        qi = (qhi * 32768 + y // 65536) % N
        a = lca(val, left, right, root, vals[pi], vals[qi])
        sink = (sink + a) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
