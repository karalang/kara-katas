# LeetCode #2257: Count Unguarded Cells in the Grid -- the benchmark's
# Python mirror of unguarded.kara: a grid of marks and a walk from every
# guard in each of the four directions until a wall, a guard or the edge.


def count_unguarded(m, n, guards, walls):
    # 0 empty, 1 seen, 2 guard, 3 wall
    grid = [[0] * n for _ in range(m)]
    for g in guards:
        grid[g[0]][g[1]] = 2
    for w in walls:
        grid[w[0]][w[1]] = 3
    for g in guards:
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r = g[0] + dr
            c = g[1] + dc
            while 0 <= r < m and 0 <= c < n and grid[r][c] < 2:
                grid[r][c] = 1
                r += dr
                c += dc
    return sum(row.count(0) for row in grid)


seed = 2257


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def place(m, n, guards, walls):
    taken = [False] * (m * n)
    cells = []
    while len(cells) < guards + walls:
        k = wide_random() % (m * n)
        if not taken[k]:
            taken[k] = True
            cells.append([k // n, k % n])
    return cells[:guards], cells[guards:]


def main():
    check = 0
    shapes = [(1, 100000), (250, 400), (100000, 1)]
    for t in range(300):
        m, n = shapes[t % 3]
        guards, walls = place(m, n, 2000, 10000)
        check = (check * 31 + count_unguarded(m, n, guards, walls) + 1) % 1000000007
    print(f"300 grids of 10^5 cells: checksum {check}")


main()
