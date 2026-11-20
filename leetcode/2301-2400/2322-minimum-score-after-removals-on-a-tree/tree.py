# LeetCode #2322: Minimum Score After Removals on a Tree -- the ★ arm in
# Python. Rooted at 0, two removals are two nodes other than the root;
# one walk gives each subtree's XOR and each node's entry and exit
# times, and the three parts follow from whether one node is the
# other's ancestor. O(n^2).
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


def tree(n, top):
    nums = [next_random() % top + 1 for _ in range(n)]
    edges = []
    for i in range(1, n):
        p = next_random() % i
        if next_random() % 2 == 0:
            edges.append([p, i])
        else:
            edges.append([i, p])
    return nums, edges


def main():
    print(minimum_score([1, 5, 5, 4, 11], [[0, 1], [1, 2], [1, 3], [3, 4]]))
    print(minimum_score([5, 5, 2, 4, 4, 2], [[0, 1], [1, 2], [5, 2], [4, 3], [1, 3]]))
    print(minimum_score([3, 9, 6], [[0, 1], [1, 2]]))
    print(minimum_score([7, 1, 2, 4, 8, 16], [[0, 1], [0, 2], [3, 0], [0, 4], [5, 0]]))
    nums, edges = tree(200, 100000000)
    print(minimum_score(nums, edges))
    check = 0
    total = 0
    for _ in range(500):
        n = next_random() % 13 + 3
        nums, edges = tree(n, 30)
        score = minimum_score(nums, edges)
        check = (check * 31 + score) % 1000000007
        total += score
    print(f"500 trees: checksum {check}, {total} in all")


main()
