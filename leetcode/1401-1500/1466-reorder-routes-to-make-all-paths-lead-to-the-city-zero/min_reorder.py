# LeetCode #1466 Reorder Routes to Make All Paths Lead to the City Zero: a
# mirror of min_reorder.kara.

from collections import deque


def min_reorder(n, connections):
    # each road is listed at both its ends, marked 1 where it leads away
    # from the end it is listed at; the roads form a tree, so the search
    # out of 0 crosses each once, away from 0, and each crossed in its own
    # direction leads away and must be turned
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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def tree(n):
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
    for i in range(len(roads) - 1, 0, -1):
        j = next_random() % (i + 1)
        roads[i], roads[j] = roads[j], roads[i]
    return roads


def main():
    global seed
    f = min_reorder
    e = [f(6, [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]), f(5, [[1, 0], [1, 2], [3, 2], [3, 4]]),
         f(3, [[1, 0], [2, 0]]), f(2, [[0, 1]]), f(2, [[1, 0]]),
         f(50000, [[c, c + 1] for c in range(49999)]), f(50000, [[0, c] for c in range(1, 50000)])]
    print(" ".join(str(x) for x in e))
    seed = 1466
    most = tree(50000)
    print(f"50000 cities: {f(50000, most)}")
    total = 0
    check = 0
    for _ in range(2000):
        n = 2 + next_random() % 59
        got = f(n, tree(n))
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"2000 random trees: total {total}, checksum {check}")


main()
