# LeetCode #2322: Minimum Score After Removals on a Tree -- the bench, the
# ★ arm in Python. Rooted at 0, two removals are two nodes other than the
# root; one walk gives each subtree's XOR and each node's entry and exit
# times, and the three parts follow from whether one node is the other's
# ancestor. O(n^2).
import sys

sys.setrecursionlimit(10000)


def visit(node, parent, adjacent, nums, xor, enter, leave, clock):
    enter[node] = clock[0]
    clock[0] += 1
    xor[node] = nums[node]
    for nxt in adjacent[node]:
        if nxt != parent:
            visit(nxt, node, adjacent, nums, xor, enter, leave, clock)
            xor[node] ^= xor[nxt]
    leave[node] = clock[0]


def minimum_score(nums, edges):
    n = len(nums)
    adjacent = [[] for _ in range(n)]
    for a, b in edges:
        adjacent[a].append(b)
        adjacent[b].append(a)
    xor = [0] * n
    enter = [0] * n
    leave = [0] * n
    visit(0, -1, adjacent, nums, xor, enter, leave, [0])
    whole = xor[0]
    best = None
    for a in range(1, n):
        for b in range(a + 1, n):
            if enter[a] <= enter[b] and leave[b] <= leave[a]:
                x, y, z = xor[b], xor[a] ^ xor[b], whole ^ xor[a]
            elif enter[b] <= enter[a] and leave[a] <= leave[b]:
                x, y, z = xor[a], xor[b] ^ xor[a], whole ^ xor[b]
            else:
                x, y, z = xor[a], xor[b], whole ^ xor[a] ^ xor[b]
            score = max(x, y, z) - min(x, y, z)
            if best is None or score < best:
                best = score
    return best


seed = 2322


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 1000
    values = []
    shapes = []
    for _ in range(10):
        values.append([next_random() % 100000000 + 1 for _ in range(n)])
        shapes.append([[next_random() % i, i] for i in range(1, n)])
    check = 0
    for _ in range(30):
        for k in range(10):
            i = next_random() % n
            values[k][i] = next_random() % 100000000 + 1
            check = (check * 31 + minimum_score(values[k], shapes[k])) % 1000000007
    print(f"30 passes over 10 trees of 1000 nodes: checksum {check}")


main()
