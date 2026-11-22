# LeetCode #2814: Minimum Time Takes to Reach Destination Without Drowning
# -- the Python mirror of the ★ arm: the second each cell floods by a
# breadth-first search from every flooded cell at once, then a
# breadth-first search from the start onto cells still dry a second
# after the step.
from collections import deque

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
NEVER = 1 << 60


def minimum_seconds(land):
    n, m = len(land), len(land[0])
    flood = [[NEVER] * m for _ in range(n)]
    queue = deque()
    for r in range(n):
        for c in range(m):
            if land[r][c] == "*":
                flood[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and flood[nr][nc] == NEVER and land[nr][nc] in (".", "S"):
                flood[nr][nc] = flood[r][c] + 1
                queue.append((nr, nc))
    time = [[-1] * m for _ in range(n)]
    for r in range(n):
        for c in range(m):
            if land[r][c] == "S":
                time[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        if land[r][c] == "D":
            return time[r][c]
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < n and 0 <= nc < m and time[nr][nc] == -1 and land[nr][nc] != "X"
                    and flood[nr][nc] > time[r][c] + 1):
                time[nr][nc] = time[r][c] + 1
                queue.append((nr, nc))
    return -1


seed = 2814


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_land(n, m, flooded):
    land = []
    for _ in range(n):
        row = []
        for _ in range(m):
            roll = next_random() % 1000
            row.append("X" if roll < 200 else "*" if roll < 200 + flooded else ".")
        land.append(row)
    start = next_random() % (n * m)
    end = next_random() % (n * m - 1)
    if end >= start:
        end += 1
    land[start // m][start % m] = "S"
    land[end // m][end % m] = "D"
    return land


def main():
    print(minimum_seconds([["D", ".", "*"], [".", ".", "."], [".", "S", "."]]))
    print(minimum_seconds([["D", "X", "*"], [".", ".", "."], [".", ".", "S"]]))
    print(minimum_seconds([["D", ".", ".", ".", "*", "."], [".", "X", ".", "X", ".", "."], [".", ".", ".", ".", "S", "."]]))
    open_land = [["."] * 100 for _ in range(100)]
    open_land[0][0] = "S"
    open_land[99][99] = "D"
    print(minimum_seconds(open_land))
    open_land[0][2] = "*"
    print(minimum_seconds(open_land))
    for count, top, flooded, label in ((3000, 4, 125, "small"), (50, 59, 2, "large")):
        reached = 0
        check = 0
        for _ in range(count):
            n = next_random() % top + 2
            m = next_random() % top + 2
            a = minimum_seconds(random_land(n, m, flooded))
            reached += 1 if a >= 0 else 0
            check = (check * 31 + a + 2) % 1000000007
        print(f"{count} {label} lands: {reached} reached, checksum {check}")


main()
