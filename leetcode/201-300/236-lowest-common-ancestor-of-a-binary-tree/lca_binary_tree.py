# LeetCode 236 — LCA of a Binary Tree (oracle mirror).
import sys
sys.setrecursionlimit(10000)

def lca(nodes, cur, p, q):
    if cur == -1: return -1
    if nodes[cur][0] in (p, q): return cur
    l = lca(nodes, nodes[cur][1], p, q)
    r = lca(nodes, nodes[cur][2], p, q)
    if l != -1 and r != -1: return cur
    return l if l != -1 else r

def report(vals, lefts, rights, p, q):
    nodes = list(zip(vals, lefts, rights))
    ans = lca(nodes, 0, p, q)
    print(-1 if ans == -1 else nodes[ans][0])

def main():
    vals   = [3, 5, 1, 6, 2, 0, 8, 7, 4]
    lefts  = [1, 3, 5, -1, 7, -1, -1, -1, -1]
    rights = [2, 4, 6, -1, 8, -1, -1, -1, -1]
    for p, q in [(5,1),(5,4),(6,4),(7,4),(6,8),(7,8),(0,8)]:
        report(vals, lefts, rights, p, q)

main()
