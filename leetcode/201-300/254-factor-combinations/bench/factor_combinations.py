"""Benchmark workload for LeetCode #254 — Factor Combinations (Python; scale lane)."""
import sys

digest = 0
total = 0


def helper(remaining, start, path):
    global digest, total
    i = start
    while i * i <= remaining:
        if remaining % i == 0:
            combo = path + [i, remaining // i]
            h = 1
            for x in combo:
                h = (h * 1000003 + x) % 1000000007
            digest = (digest + h) % 1000000007
            total += 1
            path.append(i)
            helper(remaining // i, i, path)
            path.pop()
        i += 1


def main():
    hi = 150000
    for n in range(2, hi + 1):
        if n >= 4:
            helper(n, 2, [])
    print(total, digest)


sys.setrecursionlimit(10000)
main()
