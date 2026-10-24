# Benchmark: LeetCode #959 Regions Cut By Slashes -- the ★ arm, four
# triangles per cell, on grids of 30 by 30, LeetCode's largest. Mirrors
# regions_by_slashes.kara, .c, .rs and go-seq/.


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


seed = 959


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


def main():
    rounds = 300
    grids = [random_grid(30, i % 10) for i in range(100)]
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(100):
            k = regions_by_slashes(grids[(r + i) % 100])
            total += k
            check = (check * 31 + k + i) % 1000000007
    print(f"{rounds} rounds over 100 grids of 30 by 30: {total} regions, checksum {check}")


main()
