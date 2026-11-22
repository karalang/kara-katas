# LeetCode #2814: Minimum Time Takes to Reach Destination Without Drowning
# -- the bench in Python: the ★ arm over 200 lands of 100 by 100, a cell
# in five stone and one in 5000 flooded, all drawn first, then each
# answered 5 times.
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


def main():
    count, rounds, n = 200, 5, 100
    lands = []
    for _ in range(count):
        land = []
        for _ in range(n):
            row = []
            for _ in range(n):
                roll = next_random() % 10000
                row.append("X" if roll < 2000 else "*" if roll < 2002 else ".")
            land.append(row)
        start = next_random() % (n * n)
        end = next_random() % (n * n - 1)
        if end >= start:
            end += 1
        land[start // n][start % n] = "S"
        land[end // n][end % n] = "D"
        lands.append(land)
    total = 0
    check = 0
    for r in range(rounds):
        for land in lands:
            a = minimum_seconds(land)
            total += a
            check = (check * 31 + a + 2 + r) % 1000000007
    print(f"{count} lands of {n} by {n}, {rounds} rounds: seconds sum to {total}, checksum {check}")


main()
