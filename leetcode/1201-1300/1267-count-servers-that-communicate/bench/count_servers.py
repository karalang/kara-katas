# LeetCode #1267 bench, in Python: the ★ arm (the servers in each row and
# each column counted, then each server that shares its row or column with
# another counted) on 100 random 100-by-100 grids built once, a cell a
# server one time in 2 to 9, 300 rounds; every answer folded into a
# checksum.


def count_servers(grid):
    m, n = len(grid), len(grid[0])
    rows = [0] * m
    cols = [0] * n
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:
                rows[r] += 1
                cols[c] += 1
    count = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1 and (rows[r] > 1 or cols[c] > 1):
                count += 1
    return count


seed = 1267


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


grids = []
for _ in range(100):
    odds = next_random() % 8 + 2
    grids.append([[1 if next_random() % odds == 0 else 0 for _ in range(100)] for _ in range(100)])
check = 0
for rnd in range(300):
    for g in grids:
        check = (check * 131 + count_servers(g) + rnd) % 1000000007
print(f"300 rounds of 100 grids of 100 by 100: checksum {check}")
