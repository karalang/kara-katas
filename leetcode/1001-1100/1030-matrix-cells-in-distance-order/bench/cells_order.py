# LeetCode #1030: Matrix Cells in Distance Order -- bench
# Mirrors ./cells_order.kara; see ../README.md § Benchmarks.


def all_cells_dist_order(rows, cols, r_center, c_center):
    cells = [[r, c] for r in range(rows) for c in range(cols)]
    cells.sort(key=lambda cell: abs(cell[0] - r_center) + abs(cell[1] - c_center))
    return cells


seed = 1030


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 300
    centres = []
    for _ in range(count):
        r0 = next_random() % 100
        c0 = next_random() % 100
        centres.append((r0, c0))
    total = 0
    check = 0
    for r0, c0 in centres:
        cells = all_cells_dist_order(100, 100, r0, c0)
        weighted = 0
        for i, (r, c) in enumerate(cells):
            weighted += (i + 1) * (abs(r - r0) + abs(c - c0))
        total += weighted
        check = (check * 131 + weighted) % 1000000007
    print(f"{count} centres on a 100x100 grid: sum {total}, checksum {check}")


main()
