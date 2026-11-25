# LeetCode #1349 -- Python mirror of the ★ arm: each row's students as a
# bit mask, best[mask] the most students so far with the last row seated
# as mask.


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


seed = [1349]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def grid(rows):
    return [list(r) for r in rows]


def main():
    e1 = max_students(grid(["#.##.#", ".####.", "#.##.#"]))
    e2 = max_students(grid([".#", "##", "#.", "##", ".#"]))
    e3 = max_students(grid(["#...#", ".#.#.", "..#..", ".#.#.", "#...#"]))
    one = max_students(grid(["."]))
    none = max_students(grid(["###", "###"]))
    open_ = [["."] * 8 for _ in range(8)]
    cross = [["#" if j == i else "." for j in range(8)] for i in range(8)]
    print(e1, e2, e3, one, none, max_students(open_), max_students(cross))
    total = 0
    check = 0
    for c in range(2000):
        m = 1 + next_random() % 8
        n = 1 + next_random() % 8
        broken = 2 if c % 3 == 0 else 4 if c % 3 == 1 else 0
        seats = []
        for _ in range(m):
            r = []
            for _ in range(n):
                bad = broken > 0 and next_random() % broken == 0
                r.append("#" if bad else ".")
            seats.append(r)
        got = max_students(seats)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random rooms: {total} students in all, checksum {check}")


main()
