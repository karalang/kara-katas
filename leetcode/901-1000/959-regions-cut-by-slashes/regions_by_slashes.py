# LeetCode #959: Regions Cut By Slashes -- four triangles per cell.
#
# Mirrors regions_by_slashes.kara: every cell cut along both diagonals
# into four triangles (top, right, bottom, left), joined in a union-find
# by the cell's character and across neighbouring cells; the regions are
# the sets left.


def find(parent, x):
    r = x
    while parent[r] != r:
        r = parent[r]
    while parent[x] != r:
        parent[x], x = r, parent[x]
    return r


def regions_by_slashes(grid):
    n = len(grid)
    parent = list(range(4 * n * n))
    sets = 4 * n * n

    def union(a, b):
        nonlocal sets
        ra, rb = find(parent, a), find(parent, b)
        if ra != rb:
            parent[ra] = rb
            sets -= 1

    for r in range(n):
        for c in range(n):
            # triangles 0 top, 1 right, 2 bottom, 3 left
            t = 4 * (r * n + c)
            ch = grid[r][c]
            if ch == " ":
                union(t, t + 1)
                union(t + 1, t + 2)
                union(t + 2, t + 3)
            elif ch == "/":
                union(t, t + 3)
                union(t + 1, t + 2)
            else:
                union(t, t + 1)
                union(t + 2, t + 3)
            if c + 1 < n:
                union(t + 1, t + 4 + 3)
            if r + 1 < n:
                union(t + 2, t + 4 * n)
    return sets


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(n, blank):
    grid = []
    for _ in range(n):
        row = ""
        for _ in range(n):
            if next_random() % 10 < blank:
                row += " "
            elif next_random() % 2 == 0:
                row += "/"
            else:
                row += "\\"
        grid.append(row)
    return grid


def tiled(n, pattern):
    k = len(pattern)
    return ["".join(pattern[r % k][c % k] for c in range(n)) for r in range(n)]


def show(p):
    return "[" + ", ".join(p) + "]"


def main():
    global seed
    cases = [
        [" /", "/ "],
        [" /", "  "],
        ["/\\", "\\/"],
        [" "],
        ["/"],
        ["\\"],
        ["\\/", "/\\"],
        ["//", "//"],
        [" /\\ ", "/  \\", "\\  /", " \\/ "],
        ["/\\/", "\\/\\", "/\\/"],
    ]
    for i, c in enumerate(cases):
        print(f"case {i + 1}: {regions_by_slashes(c)}")
    seed = 959
    cells = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 10
        blank = next_random() % 10
        r = regions_by_slashes(random_grid(n, blank))
        cells += n * n
        total += r
        check = (check * 31 + r) % 1000000007
    print(f"300 random grids of {cells} cells, regions: {total}, checksum {check}")
    for blank in [0, 3, 6, 9]:
        r = regions_by_slashes(random_grid(30, blank))
        print(f"30 by 30, blank {blank} in 10, regions: {r}")
    for p in [["/"], ["\\"], ["/\\", "\\/"], ["\\/", "/\\"], [" "]]:
        print(f"30 by 30 of {show(p)}, regions: {regions_by_slashes(tiled(30, p))}")


main()
