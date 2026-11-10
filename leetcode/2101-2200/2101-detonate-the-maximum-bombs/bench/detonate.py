# LeetCode #2101: Detonate the Maximum Bombs -- Python mirror of the ★
# arm's benchmark (detonate.kara): the same 2000 fields of 100 bombs,
# adjacency lists and a breadth-first search from each bomb.
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


total = 0
check = 0
for _ in range(2000):
    bombs = []
    for _ in range(100):
        x = next_random() % 1000 + 1
        y = next_random() % 1000 + 1
        r = next_random() % 150 + 1
        bombs.append([x, y, r])
    got = maximum_detonation(bombs)
    total += got
    check = (check * 31 + got) % 1000000007
print(f"2000 fields: {total} bombs in all, checksum {check}")
