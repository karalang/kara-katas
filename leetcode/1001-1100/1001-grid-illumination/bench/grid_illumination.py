# Benchmark: LeetCode #1001 Grid Illumination -- the ★ arm, counts per
# line in hash maps, on grids of 10^9 by 10^9 with 20000 lamps and 20000
# queries, LeetCode's largest. Mirrors grid_illumination.kara, .c, .rs and
# go-seq/.


def grid_illumination(n, lamps, queries):
    on = set()
    rows = {}
    cols = {}
    diags = {}
    antis = {}
    for lamp in lamps:
        r, c = lamp[0], lamp[1]
        if r * n + c not in on:
            on.add(r * n + c)
            rows[r] = rows.get(r, 0) + 1
            cols[c] = cols.get(c, 0) + 1
            diags[r - c] = diags.get(r - c, 0) + 1
            antis[r + c] = antis.get(r + c, 0) + 1
    ans = []
    for q in queries:
        r, c = q[0], q[1]
        lit = (rows.get(r, 0) > 0 or cols.get(c, 0) > 0
               or diags.get(r - c, 0) > 0 or antis.get(r + c, 0) > 0)
        ans.append(1 if lit else 0)
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if 0 <= i < n and 0 <= j < n and i * n + j in on:
                    on.remove(i * n + j)
                    rows[i] = rows.get(i, 0) - 1
                    cols[j] = cols.get(j, 0) - 1
                    diags[i - j] = diags.get(i - j, 0) - 1
                    antis[i + j] = antis.get(i + j, 0) - 1
    return ans


seed = 1001


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    rounds = 1
    n = 1000000000
    # 20 cases, each with 20000 lamps in a window of 100000 by 100000
    # cells at a random place in the grid, and 20000 queries, half of them
    # anywhere in the window and half on or beside a random lamp
    all_lamps = []
    all_queries = []
    for _ in range(20):
        top = 1 + big_random() % (n - 100002)
        left = 1 + big_random() % (n - 100002)
        lamps = []
        for _ in range(20000):
            r = top + big_random() % 100000
            c = left + big_random() % 100000
            lamps.append([r, c])
        queries = []
        for q in range(20000):
            if q % 2 == 0:
                r = top + big_random() % 100000
                c = left + big_random() % 100000
                queries.append([r, c])
            else:
                lamp = lamps[next_random() % 20000]
                r = lamp[0] + next_random() % 3 - 1
                queries.append([r, lamp[1] + next_random() % 3 - 1])
        all_lamps.append(lamps)
        all_queries.append(queries)
    lit = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            k = (r + i) % 20
            for a in grid_illumination(n, all_lamps[k], all_queries[k]):
                lit += a
                check = (check * 31 + a + 1) % 1000000007
    print(f"{rounds} rounds over 20 grids of 20000 lamps and 20000 queries: "
          f"{lit} lit, checksum {check}")


main()
