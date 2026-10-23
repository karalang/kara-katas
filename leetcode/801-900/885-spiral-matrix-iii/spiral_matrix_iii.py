# LeetCode #885: Spiral Matrix III -- Python mirror of the walking
# solution in spiral_matrix_iii.kara, with the same test harness.
#
# The spiral from the start goes east 1, south 1, west 2, north 2, east
# 3, south 3, and on: two legs of each length, turning right after each
# leg. Walking it a step at a time, off the grid as well as on it, and
# keeping each position inside the grid, gives every one of the rows *
# cols positions in order. The walk leaves the grid at most max(rows,
# cols) rings out, so it takes O(max(rows, cols)^2) steps.


def spiral_matrix_iii(rows, cols, r_start, c_start):
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    out = [[r_start, c_start]]
    r = r_start
    c = c_start
    d = 0
    length = 1
    while len(out) < rows * cols:
        for _ in range(2):
            for _ in range(length):
                r += dr[d]
                c += dc[d]
                if 0 <= r < rows and 0 <= c < cols:
                    out.append([r, c])
            d = (d + 1) % 4
        length += 1
    return out


# ---- test harness ----------------------------------------------------------


def fold(check, cells):
    c = check
    for r, col in cells:
        c = (c * 131 + r * 101 + col + 1) % 1000000007
    return c


def show(rows, cols, r_start, c_start):
    cells = spiral_matrix_iii(rows, cols, r_start, c_start)
    if len(cells) <= 12:
        shown = "[" + ", ".join(f"[{r}, {c}]" for r, c in cells) + "]"
    else:
        shown = "[" + "".join(f"[{r}, {c}], " for r, c in cells[:4])
        shown += f"... [{cells[-1][0]}, {cells[-1][1]}]] ({len(cells)} cells, checksum {fold(0, cells)})"
    print(f"rows = {rows}, cols = {cols}, rStart = {r_start}, cStart = {c_start} -> {shown}")


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    show(1, 4, 0, 0)
    show(5, 6, 1, 4)
    show(1, 1, 0, 0)
    show(3, 3, 1, 1)
    show(2, 2, 1, 1)
    show(4, 1, 2, 0)
    show(1, 5, 0, 2)
    show(100, 100, 0, 0)
    show(100, 100, 99, 99)
    show(100, 1, 37, 0)
    # small cases
    seed = 885
    cells = 0
    check = 0
    for _ in range(2000):
        rows = next_random() % 8 + 1
        cols = next_random() % 8 + 1
        r_start = next_random() % rows
        c_start = next_random() % cols
        out = spiral_matrix_iii(rows, cols, r_start, c_start)
        cells += len(out)
        check = fold(check, out)
    print(f"2000 grids of up to 8 x 8: {cells} cells, checksum {check}")
    # LeetCode's sizes: up to 100 x 100
    cells = 0
    check = 0
    for _ in range(100):
        rows = next_random() % 100 + 1
        cols = next_random() % 100 + 1
        r_start = next_random() % rows
        c_start = next_random() % cols
        out = spiral_matrix_iii(rows, cols, r_start, c_start)
        cells += len(out)
        check = fold(check, out)
    print(f"100 grids of up to 100 x 100: {cells} cells, checksum {check}")


main()
