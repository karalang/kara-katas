# LeetCode #1568: Minimum Number of Days to Disconnect Island -- the Python
# mirror of the ★ arm (days.kara): the islands counted by a walk on a
# stack, then each land cell taken away in turn. O((m n)^2)


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


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most):
    check = 0
    days = [0, 0, 0]
    for _ in range(count):
        rows = next_random() % most + 1
        cols = next_random() % most + 1
        share = next_random() % 4 + 6
        grid = []
        for _ in range(rows):
            grid.append([1 if next_random() % 10 < share else 0 for _ in range(cols)])
        answer = min_days(grid)
        days[answer] += 1
        check = mix(check, answer * 1000 + rows * 31 + cols)
    print(f"{count} grids of up to {most} by {most}: {days[0]} need 0 days, {days[1]} need 1, {days[2]} need 2, checksum {check}")


def main():
    global seed
    examples = [
        [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
        [[1, 1]],
        [[1]],
        [[0, 0]],
        [[1, 0, 1]],
        [[1, 1, 1]],
        [[1, 1], [1, 1]],
        [[1, 1, 0], [0, 1, 1]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
    ]
    for grid in examples:
        print(f"{grid} -> {min_days(grid)}")
    seed = 1568
    batch(3000, 4)
    batch(300, 10)
    batch(30, 30)


main()
