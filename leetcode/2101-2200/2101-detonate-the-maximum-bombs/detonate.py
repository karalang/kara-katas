# LeetCode #2101: Detonate the Maximum Bombs -- Python mirror of the ★ arm
# (detonate.kara): adjacency lists of which bomb sets off which, and a
# breadth-first search from each bomb. Prints the same lines.
from collections import deque


def maximum_detonation(bombs):
    n = len(bombs)
    reach = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = bombs[i][0] - bombs[j][0]
            dy = bombs[i][1] - bombs[j][1]
            if i != j and dx * dx + dy * dy <= bombs[i][2] * bombs[i][2]:
                reach[i].append(j)
    best = 0
    for start in range(n):
        seen = [False] * n
        seen[start] = True
        queue = deque([start])
        count = 0
        while queue:
            i = queue.popleft()
            count += 1
            for j in reach[i]:
                if not seen[j]:
                    seen[j] = True
                    queue.append(j)
        best = max(best, count)
    return best


seed = 2101


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def show(v):
    return "[" + ", ".join(show(x) if isinstance(x, list) else str(x) for x in v) + "]"


examples = [
    [[2, 1, 3], [6, 1, 4]],
    [[1, 1, 5], [10, 10, 5]],
    [[1, 2, 3], [2, 3, 1], [3, 4, 2], [4, 5, 3], [5, 6, 4]],
    [[7, 7, 9]],
    [[1, 1, 5], [4, 5, 1]],
    [[1, 1, 1], [1, 3, 1]],
    [[1, 1, 2], [3, 1, 2], [5, 1, 2], [7, 1, 1], [9, 1, 9]],
]
for bombs in examples:
    print(f"{show(bombs)} -> {maximum_detonation(bombs)}")
total = 0
check = 0
for rnd in range(3000):
    n = next_random() % 12 + 1
    bombs = []
    for _ in range(n):
        if rnd % 2 == 0:
            x = next_random() % 20 + 1
            y = next_random() % 20 + 1
            r = next_random() % 8 + 1
        else:
            x = wide_random() % 100000 + 1
            y = wide_random() % 100000 + 1
            r = wide_random() % 100000 + 1
        bombs.append([x, y, r])
    got = maximum_detonation(bombs)
    total += got
    check = (check * 31 + got) % 1000000007
print(f"3000 fields: {total} bombs in all, checksum {check}")
chain = []
at = 1
for i in range(100):
    gap = 1000 - 5 * i
    chain.append([at, 50000, gap])
    at += gap
print(f"a chain of 100: {maximum_detonation(chain)}")
back = []
at = 1
behind = 1
for i in range(100):
    back.append([at, 50000, behind])
    behind = 500 + 5 * i
    at += behind
print(f"a chain of 100 set off from its far end: {maximum_detonation(back)}")
apart = [[1 + 1000 * (i % 10), 1 + 1000 * (i // 10), 999] for i in range(100)]
print(f"100 apart: {maximum_detonation(apart)}")
corners = [[1 if i % 2 == 0 else 100000, 1 if i % 4 < 2 else 100000, 100000] for i in range(100)]
print(f"100 at the corners: {maximum_detonation(corners)}")
