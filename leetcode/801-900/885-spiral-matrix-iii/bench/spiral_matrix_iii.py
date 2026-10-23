# LeetCode #885 bench: Python mirror of spiral_matrix_iii.kara (the ★
# arm, walking the spiral) on the same 6000 grids.


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


seed = 885


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cells = 0
    check = 0
    for _ in range(6000):
        # 50 x 50 to 100 x 100, the start anywhere
        rows = 50 + next_random() % 51
        cols = 50 + next_random() % 51
        r_start = next_random() % rows
        c_start = next_random() % cols
        out = spiral_matrix_iii(rows, cols, r_start, c_start)
        cells += len(out)
        last = out[-1]
        check = (check * 131 + last[0] * 101 + last[1] + out[len(out) // 2][0]) % 1000000007
    print(f"6000 grids of up to 100 x 100: {cells} cells, checksum {check}")


main()
