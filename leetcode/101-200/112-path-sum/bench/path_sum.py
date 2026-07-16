#!/usr/bin/env python3
# Benchmark workload for LeetCode #112 — path sum, Python mirror.
# Runs a SMALLER K (pure-Python recursion is slow); timed separately, NOT cross-checked.
import sys
MOD = 1000000007
class Node:
    __slots__ = ("val", "left", "right")
    def __init__(self, val):
        self.val = val; self.left = None; self.right = None
def build(lo, hi):
    if lo > hi: return None
    mid = (lo + hi) // 2
    n = Node(mid); n.left = build(lo, mid - 1); n.right = build(mid + 1, hi); return n
def has_path_sum(n, target):
    if n is None: return False
    rem = target - n.val
    if n.left is None and n.right is None: return rem == 0
    return has_path_sum(n.left, rem) or has_path_sum(n.right, rem)
def main():
    pool = [build(t * 100, t * 100 + 30) for t in range(8)]
    acc = 1; K = 300000
    for _ in range(K):
        idx = acc % 8
        hit = has_path_sum(pool[idx], 1000000000)
        acc = (acc * 131 + (1 if hit else 0) + 1) % MOD
    print(acc)
if __name__ == "__main__":
    sys.setrecursionlimit(10000); main()
