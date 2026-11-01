# LeetCode #1030: Matrix Cells in Distance Order -- sorted by distance
# Mirrors cells_order.kara (the ★ arm) and prints the same output.


def all_cells_dist_order(rows, cols, r_center, c_center):
    cells = [[r, c] for r in range(rows) for c in range(cols)]
    cells.sort(key=lambda cell: abs(cell[0] - r_center) + abs(cell[1] - c_center))
    return cells


seed = 1030


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def distance(cell, r_center, c_center):
    return abs(cell[0] - r_center) + abs(cell[1] - c_center)


def in_order(cells, r_center, c_center):
    return all(distance(cells[i - 1], r_center, c_center) <= distance(cells[i], r_center, c_center)
               for i in range(1, len(cells)))


def canonical(cells, r_center, c_center):
    return sorted(cells, key=lambda cell: (distance(cell, r_center, c_center), cell[0], cell[1]))


def show(cells):
    return "[" + ",".join(f"[{r},{c}]" for r, c in cells) + "]"


def fold(check, cells):
    h = check
    for r, c in cells:
        h = (h * 131 + r * 101 + c + 1) % 1000000007
    return h


def main():
    examples = [
        (1, 2, 0, 0), (2, 2, 0, 1), (2, 3, 1, 2),
        (1, 1, 0, 0), (3, 3, 1, 1), (1, 5, 0, 2), (4, 1, 3, 0), (3, 4, 2, 0),
    ]
    for rows, cols, r0, c0 in examples:
        cells = all_cells_dist_order(rows, cols, r0, c0)
        order = "in order" if in_order(cells, r0, c0) else "OUT OF ORDER"
        print(f"{rows}x{cols} from ({r0},{c0}): {show(canonical(cells, r0, c0))} {order}")
    groups = [(3000, 3, 3), (1000, 8, 8), (300, 20, 5), (100, 30, 30), (20, 100, 100), (10, 1, 100)]
    for count, top_r, top_c in groups:
        total = 0
        out_of_order = 0
        check = 0
        for _ in range(count):
            rows = next_random() % top_r + 1
            cols = next_random() % top_c + 1
            r0 = next_random() % rows
            c0 = next_random() % cols
            cells = all_cells_dist_order(rows, cols, r0, c0)
            total += len(cells)
            if not in_order(cells, r0, c0):
                out_of_order += 1
            check = fold(check, canonical(cells, r0, c0))
        print(f"{count} grids up to {top_r}x{top_c}: {total} cells, {out_of_order} out of order, checksum {check}")
    for r0, c0 in [(0, 0), (99, 99), (50, 50), (0, 73)]:
        cells = all_cells_dist_order(100, 100, r0, c0)
        canon = canonical(cells, r0, c0)
        last = canon[-1]
        order = "in order" if in_order(cells, r0, c0) else "OUT OF ORDER"
        print(f"100x100 from ({r0},{c0}): {len(cells)} cells {order}, farthest [{last[0]},{last[1]}] "
              f"at {distance(last, r0, c0)}, checksum {fold(0, canon)}")


main()
