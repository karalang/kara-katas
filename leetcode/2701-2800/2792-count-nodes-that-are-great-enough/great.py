# LeetCode #2792: Count Nodes That Are Great Enough -- the ★ arm in Python
# (great.kara): each node keeps its subtree's k least values, sorted,
# from its children's and its own, the nodes taken children first.
from collections import deque


def count_great_enough_nodes(vals, left, right, k):
    n = len(vals)
    order = []
    stack = [0]
    while stack:
        u = stack.pop()
        order.append(u)
        for c in (left[u], right[u]):
            if c >= 0:
                stack.append(c)
    least = [[] for _ in range(n)]
    great = 0
    for u in reversed(order):
        mine = [vals[u]]
        for c in (left[u], right[u]):
            if c >= 0:
                mine.extend(least[c])
        mine.sort()
        del mine[k:]
        if len(mine) == k and mine[k - 1] < vals[u]:
            great += 1
        least[u] = mine
    return great


seed = 2792


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def level(lst):
    vals = [v for v in lst if v >= 0]
    n = len(vals)
    left = [-1] * n
    right = [-1] * n
    queue = deque([0])
    nxt = 1
    at = 1
    while queue:
        u = queue.popleft()
        for side in range(2):
            if at < len(lst):
                if lst[at] >= 0:
                    if side == 0:
                        left[u] = nxt
                    else:
                        right[u] = nxt
                    queue.append(nxt)
                    nxt += 1
                at += 1
    return vals, left, right


def random_tree(n, top):
    vals = [next_random() % top + 1 for _ in range(n)]
    left = [-1] * n
    right = [-1] * n
    for i in range(1, n):
        placed = False
        while not placed:
            p = next_random() % i
            if next_random() % 2 == 0:
                if left[p] < 0:
                    left[p] = i
                    placed = True
            elif right[p] < 0:
                right[p] = i
                placed = True
    return vals, left, right


def main():
    print(count_great_enough_nodes(*level([7, 6, 5, 4, 3, 2, 1]), 2))
    print(count_great_enough_nodes(*level([1, 2, 3]), 1))
    print(count_great_enough_nodes(*level([3, 2, 2]), 2))
    n = 10000
    down = [i + 1 if i + 1 < n else -1 for i in range(n)]
    none = [-1] * n
    print(count_great_enough_nodes([n - i for i in range(n)], down, none, 10))
    print(count_great_enough_nodes([i + 1 for i in range(n)], down, none, 10))
    total = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 12 + 1
        v, l, r = random_tree(m, 5)
        k = next_random() % 4 + 1
        a = count_great_enough_nodes(v, l, r, k)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 small trees: great enough sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(20):
        v, l, r = random_tree(n, 10000)
        k = next_random() % 10 + 1
        a = count_great_enough_nodes(v, l, r, k)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"20 trees of 10^4: great enough sum to {total}, checksum {check}")


main()
