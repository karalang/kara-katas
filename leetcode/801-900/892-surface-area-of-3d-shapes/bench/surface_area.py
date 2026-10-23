# LeetCode #892 bench: Python mirror of surface_area.kara (the ★ arm, six
# faces a cube, less the shared ones) on the same 400 grids and 80 passes.


def surface_area(grid):
    n = len(grid)
    area = 0
    for i in range(n):
        for j in range(n):
            v = grid[i][j]
            if v > 0:
                area += 4 * v + 2
            if i + 1 < n:
                area -= 2 * min(v, grid[i + 1][j])
            if j + 1 < n:
                area -= 2 * min(v, grid[i][j + 1])
    return area


def main():
    seed = 892

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    grids = [[[next_random() % 51 for _ in range(50)] for _ in range(50)] for _ in range(400)]
    total = 0
    check = 0
    for p in range(80):
        for g in range(len(grids)):
            i = (p * 7 + g) % 50
            j = (p * 13 + g * 3) % 50
            grids[g][i][j] += 1
            got = surface_area(grids[g])
            total += got
            check = (check * 131 + got) % 1000000007
    print(f"32000 measurements of 400 grids of 50 by 50: surface area {total}, checksum {check}")


main()
