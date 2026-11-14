# LeetCode #1568: Minimum Number of Days to Disconnect Island -- bench:
# the ★ arm (each land cell taken away in turn) over 20 grids of 30 by 30,
# built once, all land but for a water cell one time in 20; 5 passes, each
# first turning one cell of every grid over.


def islands(grid):
    rows = len(grid)
    cols = len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not seen[r][c]:
                count += 1
                seen[r][c] = True
                stack = [(r, c)]
                while stack:
                    i, j = stack.pop()
                    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        a, b = i + di, j + dj
                        if 0 <= a < rows and 0 <= b < cols and grid[a][b] == 1 and not seen[a][b]:
                            seen[a][b] = True
                            stack.append((a, b))
    return count


def min_days(grid):
    if islands(grid) != 1:
        return 0
    grid = [row[:] for row in grid]
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1:
                grid[r][c] = 0
                split = islands(grid) != 1
                grid[r][c] = 1
                if split:
                    return 1
    return 2


seed = 1568


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 30
    passes = 5
    grids = []
    for _ in range(20):
        grid = []
        for _ in range(n):
            grid.append([0 if next_random() % 20 == 0 else 1 for _ in range(n)])
        grids.append(grid)
    check = 0
    days = [0, 0, 0]
    for p in range(passes):
        for g in range(len(grids)):
            at = (p * 7919 + g * 104729) % (n * n)
            grids[g][at // n][at % n] = 1 - grids[g][at // n][at % n]
            answer = min_days(grids[g])
            days[answer] += 1
            check = mix(check, answer)
    print(f"{passes} passes over 20 grids of 30 by 30: {days[0]} need 0 days, {days[1]} need 1, {days[2]} need 2, checksum {check}")


main()
