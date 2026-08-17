"""Benchmark workload for LeetCode #257 — Binary Tree Paths (Python; scale lane)."""
import sys


def main():
    n = 150000
    rounds = 5

    val, left, right = [], [], []
    open_ = []
    state = 257257

    state = (state * 1103515245 + 12345) & 2147483647
    val.append((state // 65536) % 100 - 50); left.append(-1); right.append(-1)
    open_.append(0)

    while len(val) < n:
        state = (state * 1103515245 + 12345) & 2147483647
        wd0 = state // 65536
        state = (state * 1103515245 + 12345) & 2147483647
        pick = (wd0 * 32768 + state // 65536) % len(open_)
        parent = open_[pick]
        state = (state * 1103515245 + 12345) & 2147483647
        val.append((state // 65536) % 100 - 50); left.append(-1); right.append(-1)
        child = len(val) - 1
        if left[parent] == -1:
            left[parent] = child
        else:
            right[parent] = child
            open_[pick] = open_[-1]
            open_.pop()
        open_.append(child)

    sink = 0
    for _ in range(rounds):
        out = []
        stack = [(0, str(val[0]))]
        # iterative to avoid Python's recursion limit; same visit order as the
        # .kara recursion (right pushed first so left is processed first)
        while stack:
            node, prefix = stack.pop()
            l, r = left[node], right[node]
            if l == -1 and r == -1:
                out.append(prefix)
            else:
                if r != -1:
                    stack.append((r, prefix + "->" + str(val[r])))
                if l != -1:
                    stack.append((l, prefix + "->" + str(val[l])))

        h = 1
        for s in out:
            for b in s.encode():
                h = (h * 1000003 + b) % 1000000007
            h = (h * 31 + 7) % 1000000007
        sink = (sink * 131 + h) % 1000000007
    print(sink)


sys.setrecursionlimit(100000)
main()
