# LeetCode #1349 bench -- Python: each row's students as a bit mask,
# best[mask] the most students so far with the last row seated as mask.


def max_students(seats):
    n = len(seats[0])
    full = 1 << n
    best = [-1] * full
    best[0] = 0
    for row in seats:
        good = 0
        for j in range(n):
            if row[j] == ".":
                good |= 1 << j
        nxt = [-1] * full
        for mask in range(full):
            if mask & good != mask or mask & (mask << 1):
                continue
            here = bin(mask).count("1")
            for prev in range(full):
                if best[prev] < 0 or mask & (prev << 1) or mask & (prev >> 1):
                    continue
                nxt[mask] = max(nxt[mask], best[prev] + here)
        best = nxt
    return max(best)


def main():
    seed = 1349
    rooms = []
    for _ in range(20):
        seats = []
        for _ in range(8):
            r = []
            for _ in range(8):
                seed = (seed * 1103515245 + 12345) % 2147483648
                r.append("#" if (seed // 65536) % 4 == 0 else ".")
            seats.append(r)
        rooms.append(seats)
    check = 0
    for r in range(3000):
        k = check % 20
        i = (check // 20) % 8
        j = (check // 160) % 8
        rooms[k][i][j] = "#" if rooms[k][i][j] == "." else "."
        check = (check * 31 + max_students(rooms[k]) + r) % 1000000007
    print(f"3000 rounds over 20 rooms of 8 by 8: checksum {check}")


main()
