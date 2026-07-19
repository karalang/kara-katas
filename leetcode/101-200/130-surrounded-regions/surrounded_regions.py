"""LeetCode #130: Surrounded Regions — Python oracle.

Flip every 'O' NOT connected to the border to 'X'. Grid as ints: 0='X', 1='O'.
Flood-fill from every border 'O' marking the border-connected component safe (2),
then: safe->'O'(1), any remaining 1->'X'(0). Report a hash of the final grid.
"""


def solve(grid):
    rows = len(grid)
    if rows == 0:
        return grid
    cols = len(grid[0])

    def flood(sr, sc):
        stack = [(sr, sc)]
        while stack:
            r, c = stack.pop()
            if r < 0 or r >= rows or c < 0 or c >= cols:
                continue
            if grid[r][c] != 1:
                continue
            grid[r][c] = 2  # safe
            stack.append((r + 1, c))
            stack.append((r - 1, c))
            stack.append((r, c + 1))
            stack.append((r, c - 1))

    for r in range(rows):
        for c in range(cols):
            on_border = r == 0 or r == rows - 1 or c == 0 or c == cols - 1
            if on_border and grid[r][c] == 1:
                flood(r, c)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                grid[r][c] = 1
            elif grid[r][c] == 1:
                grid[r][c] = 0
    return grid


def grid_hash(grid):
    MOD = 1000000007
    h = 0
    for row in grid:
        for v in row:
            h = (h * 131 + v + 1) % MOD
        h = (h * 131 + 7) % MOD
    return h


def build(rows, cols, seed):
    g = []
    x = seed
    for _ in range(rows):
        row = []
        for _ in range(cols):
            x = (x * 1103515245 + 12345) % 2147483648
            row.append(1 if (x % 3) != 0 else 0)  # ~2/3 'O'
        g.append(row)
    return g


def main():
    MOD = 1000000007
    sink = 0
    # A hand case: a single interior O ring captured, border O safe.
    g0 = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ]
    sink = (sink * 1000003 + grid_hash(solve(g0))) % MOD
    for t in range(6):
        g = build(5 + t, 6 + t, t + 1)
        sink = (sink * 1000003 + grid_hash(solve(g))) % MOD
    print(f"sink: {sink}")


if __name__ == "__main__":
    main()
