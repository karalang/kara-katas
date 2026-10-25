# LeetCode #1001: Grid Illumination -- mirror of the ★ arm
# (grid_illumination.kara), counts per line in hash maps.


def grid_illumination(n, lamps, queries):
    on = set()
    rows = {}
    cols = {}
    diags = {}
    antis = {}
    for r, c in lamps:
        if r * n + c not in on:
            on.add(r * n + c)
            rows[r] = rows.get(r, 0) + 1
            cols[c] = cols.get(c, 0) + 1
            diags[r - c] = diags.get(r - c, 0) + 1
            antis[r + c] = antis.get(r + c, 0) + 1
    ans = []
    for r, c in queries:
        lit = rows.get(r, 0) > 0 or cols.get(c, 0) > 0 or diags.get(r - c, 0) > 0 or antis.get(r + c, 0) > 0
        ans.append(1 if lit else 0)
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if 0 <= i < n and 0 <= j < n and i * n + j in on:
                    on.remove(i * n + j)
                    rows[i] -= 1
                    cols[j] -= 1
                    diags[i - j] -= 1
                    antis[i + j] -= 1
    return ans


seed = 1001


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random(m):
    # a random number from 0 to m - 1, for m up to 2^30
    return (next_random() * 32768 + next_random()) % m


# a grid of n from lo to hi, and lamps and queries in a random window of
# up to `wide` by `wide` cells somewhere in it, so that they share lines
def random_case(lo, hi, wide, most):
    n = lo + big_random(hi - lo + 1)
    w = min(n, 1 + next_random() % wide)
    top = big_random(n - w + 1)
    left = big_random(n - w + 1)
    lamps = [[top + next_random() % w, left + next_random() % w] for _ in range(next_random() % (most + 1))]
    queries = [[top + next_random() % w, left + next_random() % w] for _ in range(1 + next_random() % most)]
    return n, lamps, queries


def text(rows):
    return "[" + ",".join("[" + ",".join(str(x) for x in row) + "]" for row in rows) + "]"


def main():
    cases = [
        (5, [[0, 0], [4, 4]], [[1, 1], [1, 0]]),
        (5, [[0, 0], [4, 4]], [[1, 1], [1, 1]]),
        (5, [[0, 0], [0, 4]], [[0, 4], [0, 1], [1, 4]]),
        (1, [[0, 0]], [[0, 0], [0, 0]]),
        (3, [], [[1, 1]]),
        (3, [[1, 1], [1, 1]], [[0, 0], [2, 2], [0, 0]]),
        (4, [[0, 0]], [[3, 3], [2, 1], [1, 1], [3, 3]]),
        (4, [[0, 3], [3, 0]], [[1, 2], [2, 2], [3, 3]]),
        (6, [[2, 2], [2, 4], [4, 2]], [[3, 3], [0, 0], [5, 5]]),
        (1000000000, [[0, 0], [999999999, 999999999]], [[500000000, 500000000], [999999998, 999999998], [999999999, 0]]),
    ]
    for n, lamps, queries in cases:
        ans = grid_illumination(n, lamps, queries)
        print(f"n = {n}, lamps = {text(lamps)}, queries = {text(queries)} -> [{','.join(str(x) for x in ans)}]")
    groups = [(300, 1, 6, 6, 6), (3000, 1, 30, 30, 40), (300, 1000000, 1000000000, 30, 200),
              (2, 50, 50, 50, 2000), (2, 1000000000, 1000000000, 100, 2000)]
    for count, lo, hi, wide, most in groups:
        lit = 0
        asked = 0
        check = 0
        for _ in range(count):
            n, lamps, queries = random_case(lo, hi, wide, most)
            for a in grid_illumination(n, lamps, queries):
                lit += a
                check = (check * 31 + a + 1) % 1000000007
            asked += len(queries)
        print(f"{count} random grids, {asked} queries: {lit} lit, checksum {check}")

main()
