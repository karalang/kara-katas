# Python mirror of cells.kara (LeetCode #2194, the ★ arm): two loops over
# the range's bytes, the column outside and the row inside.


def cells_in_range(s):
    b = s.encode()
    return [bytes([col, row]).decode() for col in range(b[0], b[3] + 1) for row in range(b[1], b[4] + 1)]


def show(s):
    print(f"{s} -> [{', '.join(cells_in_range(s))}]")


for s in ["K1:L2", "A1:F1", "C7:C7", "Z1:Z9", "B5:E5", "A1:Z9"]:
    show(s)
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ranges = cells = check = 0
for c1 in range(26):
    for c2 in range(c1, 26):
        for r1 in range(1, 10):
            for r2 in range(r1, 10):
                got = cells_in_range(f"{letters[c1]}{r1}:{letters[c2]}{r2}")
                ranges += 1
                cells += len(got)
                for cell in got:
                    for b in cell.encode():
                        check = (check * 31 + b) % 1000000007
print(f"{ranges} ranges: {cells} cells, checksum {check}")
