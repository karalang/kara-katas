# LeetCode 808 -- Soup Servings: mirrors the harness of soup_servings.kara
# with the ★ arm's table built bottom up.


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
    for n in [50, 100, 0, 1, 25, 26, 4800, 4801, 1000000000]:
        print(f"n = {n}: {soup_servings(n):.5f}")
    line = "every 25 ml to 300:"
    n = 25
    while n <= 300:
        line += f" {soup_servings(n):.5f}"
        n += 25
    print(line)
    m = 0
    while soup_servings(25 * m) <= 0.99999:
        m += 1
    print(f"first above 0.99999: {25 * m} ml, {soup_servings(25 * m):.7f}")
    total = 0.0
    count = 0
    n = 0
    while n <= 5000:
        total += soup_servings(n)
        count += 1
        n += 37
    print(f"{count} sizes from 0 to 5000 ml: sum {total:.5f}")


main()
