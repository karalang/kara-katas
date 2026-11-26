# LeetCode #1466 bench in Python: the ★ arm (a breadth-first search out of
# city 0 over the roads taken both ways) on the same 10 trees of 50000
# cities and 20 passes.

from collections import deque


def min_reorder(n, connections):
    roads = [[] for _ in range(n)]
    for a, b in connections:
        roads[a].append((b, 1))
        roads[b].append((a, 0))
    seen = [False] * n
    queue = deque([0])
    seen[0] = True
    turned = 0
    while queue:
        city = queue.popleft()
        for nxt, away in roads[city]:
            if not seen[nxt]:
                seen[nxt] = True
                turned += away
                queue.append(nxt)
    return turned


seed = 1466


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 50000
    trees = []
    for _ in range(10):
        label = list(range(n))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            label[i], label[j] = label[j], label[i]
        roads = []
        for i in range(1, n):
            p = next_random() % i
            if next_random() % 2 == 0:
                roads.append([label[i], label[p]])
            else:
                roads.append([label[p], label[i]])
        trees.append(roads)
    check = 0
    for pass_ in range(20):
        for t in range(10):
            k = check % (n - 1)
            r = trees[t][k]
            r[0], r[1] = r[1], r[0]
            got = min_reorder(n, trees[t])
            check = (check * 31 + got + pass_) % 1000000007
    print(f"20 passes over 10 trees of 50000 cities: checksum {check}")


main()
