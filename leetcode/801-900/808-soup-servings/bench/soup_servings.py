# LeetCode 808 — Soup Servings: the bench.
#
# Each round works out the answer for a size from 3750 to 4800 ml, 150
# to 192 servings, the largest the table is built for.


def soup_servings(n):
    if n > 4800:
        return 1.0
    m = (n + 24) // 25
    p = [[0.0] * (m + 1) for _ in range(m + 1)]
    for a in range(m + 1):
        for b in range(m + 1):
            if a == 0 and b == 0:
                p[a][b] = 0.5
            elif a == 0:
                p[a][b] = 1.0
            elif b == 0:
                p[a][b] = 0.0
            else:
                s = 0.0
                for da, db in [(4, 0), (3, 1), (2, 2), (1, 3)]:
                    s += p[max(a - da, 0)][max(b - db, 0)]
                p[a][b] = 0.25 * s
    return p[m][m]


def main():
    rounds = 30000
    total = 0.0
    sure = 0
    for r in range(rounds):
        n = 3750 + (r * 37) % 1051
        p = soup_servings(n)
        total += p
        if p > 0.99999:
            sure += 1
    print(f"{rounds} rounds of 3750 to 4800 ml: sum {total:.6f}, {sure} above 0.99999")


main()
