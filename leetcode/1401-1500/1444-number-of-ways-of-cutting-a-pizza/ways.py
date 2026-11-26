# LeetCode #1444: Number of Ways of Cutting a Pizza -- the Python mirror of
# ways.kara: the apples from each row and column on, and for each count of
# pieces still to give, the ways to cut the part from each row and column on


def ways(pizza, k):
    rows = len(pizza)
    cols = len(pizza[0])
    apples = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            here = 1 if pizza[r][c] == "A" else 0
            apples[r][c] = here + apples[r + 1][c] + apples[r][c + 1] - apples[r + 1][c + 1]
    w = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            if apples[r][c] > 0:
                w[r][c] = 1
    for _ in range(1, k):
        nxt = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                total = 0
                for cut in range(r + 1, rows):
                    if apples[r][c] - apples[cut][c] > 0:
                        total += w[cut][c]
                for cut in range(c + 1, cols):
                    if apples[r][c] - apples[r][cut] > 0:
                        total += w[r][cut]
                nxt[r][c] = total % 1000000007
        w = nxt
    return w[0][0]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(rows, cols, rate):
    return ["".join("A" if next_random() % 100 < rate else "." for _ in range(cols)) for _ in range(rows)]


def main():
    global seed
    cases = [(["A..", "AAA", "..."], 3), (["A..", "AA.", "..."], 3), (["A..", "A..", "..."], 1), (["A"], 1), (["."], 1), (["A.A"], 2), (["A", "A", "A"], 3), ([".A", "A."], 2)]
    print(" ".join(str(ways(p, k)) for p, k in cases))
    seed = 1444
    full = drawn(50, 50, 100)
    sparse = drawn(50, 50, 10)
    corner = drawn(50, 50, 0)
    corner[49] = "." * 49 + "A"
    print(f"50 by 50: {ways(full, 10)} {ways(sparse, 10)} {ways(corner, 1)}")
    check = 0
    total = 0
    for _ in range(2000):
        rows = 1 + next_random() % 8
        cols = 1 + next_random() % 8
        rate = next_random() % 101
        k = 1 + next_random() % 10
        got = ways(drawn(rows, cols, rate), k)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random pizzas: {total} in all, checksum {check}")


main()
