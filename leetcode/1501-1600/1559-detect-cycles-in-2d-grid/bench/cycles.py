# LeetCode #1559: Detect Cycles in 2D Grid -- bench: the ★ arm (a search
# on a stack, each cell with the cell it came from) over 20 comb grids of
# 500 by 500 with no cycle, half with two cells made `a` to join two teeth
# in one, built once, each asked 5 times.
# Python mirror of cycles.kara.


def contains_cycle(grid):
    rows = len(grid)
    cols = len(grid[0])
    seen = [False] * (rows * cols)
    for start in range(rows * cols):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, -1)]
        while stack:
            cell, came = stack.pop()
            r, c = cell // cols, cell % cols
            for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                nr, nc = r + dr, c + dc
                if nr < 0 or nr >= rows or nc < 0 or nc >= cols or grid[nr][nc] != grid[r][c]:
                    continue
                nxt = nr * cols + nc
                if nxt == came:
                    continue
                if seen[nxt]:
                    return True
                seen[nxt] = True
                stack.append((nxt, cell))
    return False


seed = 1559


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def comb(size):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    grid = []
    for r in range(size):
        row = []
        for c in range(size):
            if r == 0 or c % 2 == 0:
                row.append("a")
            else:
                row.append(alphabet[next_random() % 25 + 1])
        grid.append(row)
    return grid


def main():
    size = 500
    grids = []
    for g in range(20):
        grid = comb(size)
        if g % 2 == 1:
            r = next_random() % (size - 2) + 1
            c = next_random() % (size // 2 - 1) * 2 + 1
            grid[r][c] = "a"
            grid[r + 1][c] = "a"
        grids.append(grid)
    check = 0
    found = 0
    for p in range(5):
        for g, grid in enumerate(grids):
            cycle = contains_cycle(grid)
            if cycle:
                found += 1
            check = mix(check, p * 20 + g if cycle else -1)
    print(f"5 passes over 20 grids of 500 by 500: {found} with a cycle, checksum {check}")


main()
