# LeetCode #2257: Count Unguarded Cells in the Grid -- Python mirror of
# unguarded.kara: guards and walls marked, then from every guard a walk in
# each direction marking what it sees until a wall, a guard or the edge.


def count_unguarded(m, n, guards, walls):
    # 0 empty, 1 seen, 2 guard, 3 wall
    grid = [[0] * n for _ in range(m)]
    for r, c in guards:
        grid[r][c] = 2
    for r, c in walls:
        grid[r][c] = 3
    for gr, gc in guards:
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r, c = gr + dr, gc + dc
            while 0 <= r < m and 0 <= c < n and grid[r][c] < 2:
                grid[r][c] = 1
                r += dr
                c += dc
    return sum(row.count(0) for row in grid)


# ---- test harness ---------------------------------------------------------

seed = 0


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


def show(cells):
    return "[" + ", ".join(f"[{r}, {c}]" for r, c in cells) + "]"


def main():
    global seed
    examples = [
        (4, 6, [[0, 0], [1, 1], [2, 3]], [[0, 1], [2, 2], [1, 4]]),
        (3, 3, [[1, 1]], [[0, 1], [1, 0], [2, 1], [1, 2]]),
        (1, 1, [[0, 0]], []),
        (1, 5, [[0, 0]], [[0, 2]]),
        (1, 5, [[0, 0], [0, 4]], []),
        (3, 4, [[1, 1]], [[0, 1], [1, 0], [1, 2], [2, 1], [0, 3]]),
    ]
    for m, n, guards, walls in examples:
        print(f"{m} x {n}, guards {show(guards)}, walls {show(walls)} -> {count_unguarded(m, n, guards, walls)}")
    seed = 2257
    total = 0
    check = 0
    for _ in range(2000):
        m = next_random() % 6 + 1
        n = next_random() % 6 + 1
        g = min(next_random() % 3 + 1, m * n)
        w = min(next_random() % 5, m * n - g)
        guards, walls = place(m, n, g, w)
        count = count_unguarded(m, n, guards, walls)
        total += count
        check = (check * 31 + count + 1) % 1000000007
    print(f"2000 grids: {total} unguarded in all, checksum {check}")
    answers = []
    for m, n in ((1, 100000), (250, 400), (100000, 1)):
        guards, walls = place(m, n, 2000, 10000)
        answers.append(count_unguarded(m, n, guards, walls))
    print(f"10^5 cells: [{', '.join(str(a) for a in answers)}]")


main()
