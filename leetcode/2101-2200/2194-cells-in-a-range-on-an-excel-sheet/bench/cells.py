# benchmark's Python mirror of cells.kara (LeetCode #2194, the ★ arm):
# two loops over the range's bytes.


def cells_in_range(s):
    b = s.encode()
    cells = []
    for col in range(b[0], b[3] + 1):
        for row in range(b[1], b[4] + 1):
            cells.append(bytes([col, row]).decode())
    return cells


def main():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ranges = [f"{letters[c1]}{r1}:{letters[c2]}{r2}" for c1 in range(26) for c2 in range(c1, 26)
              for r1 in range(1, 10) for r2 in range(r1, 10)]
    check = 0
    for _ in range(20):
        for s in ranges:
            cells = cells_in_range(s)
            last = cells[-1].encode()
            check = (check * 31 + len(cells) * 1000 + last[0] * 10 + last[1]) % 1000000007
    print(f"20 passes over {len(ranges)} ranges: checksum {check}")


main()
