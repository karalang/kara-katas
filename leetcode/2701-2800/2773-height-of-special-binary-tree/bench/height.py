# LeetCode #2773: Height of Special Binary Tree -- the bench in Python:
# the ★ arm over 20 random trees of 10^4 nodes, all drawn first, then each
# answered 200 times.
import sys

sys.setrecursionlimit(100000)


def depth(u, left, right):
    best = 0
    l = left[u]
    if l >= 0 and right[l] != u:
        best = max(best, depth(l, left, right) + 1)
    r = right[u]
    if r >= 0 and left[r] != u:
        best = max(best, depth(r, left, right) + 1)
    return best


def height_of_tree(left, right, root):
    return depth(root, left, right)


seed = 2773


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def joined(left, right, root):
    leaves = []
    stack = [root]
    while stack:
        u = stack.pop()
        if left[u] < 0 and right[u] < 0:
            leaves.append(u)
        if right[u] >= 0:
            stack.append(right[u])
        if left[u] >= 0:
            stack.append(left[u])
    l = list(left)
    r = list(right)
    k = len(leaves)
    for i in range(k):
        r[leaves[i]] = leaves[(i + 1) % k]
        l[leaves[i]] = leaves[(i + k - 1) % k]
    return l, r


def grown(n, reach):
    left = [-1] * n
    right = [-1] * n
    for k in range(1, n):
        p = k - 1 - next_random() % min(reach, k)
        while left[p] >= 0 and right[p] >= 0:
            p = next_random() % k
        if left[p] >= 0:
            go_left = False
        elif right[p] >= 0:
            go_left = True
        else:
            go_left = next_random() % 2 == 0
        if go_left:
            left[p] = k
        else:
            right[p] = k
    return joined(left, right, 0)


def main():
    count = 20
    rounds = 200
    trees = []
    for _ in range(count):
        reach = next_random() % 50 + 1
        trees.append(grown(10000, reach))
    total = 0
    check = 0
    for r in range(rounds):
        for left, right in trees:
            h = height_of_tree(left, right, 0)
            total += h
            check = (check * 31 + h + r) % 1000000007
    print(f"{count} trees of 10^4, {rounds} rounds: heights sum to {total}, checksum {check}")


main()
