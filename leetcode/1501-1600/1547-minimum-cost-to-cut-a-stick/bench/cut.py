# LeetCode #1547: Minimum Cost to Cut a Stick -- bench: the ★ arm (interval
# DP) over 100 sticks of 2 to 1000000 with 1 to 100 distinct cuts, built
# once, each asked 4 times. Python mirror of cut.kara.


def min_cost(n, cuts):
    points = sorted(cuts + [0, n])
    m = len(points)
    cost = [[0] * m for _ in range(m)]
    for gap in range(2, m):
        for i in range(m - gap):
            j = i + gap
            best = min(cost[i][k] + cost[k][j] for k in range(i + 1, j))
            cost[i][j] = best + points[j] - points[i]
    return cost[0][m - 1]


seed = 1547


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    sticks = []
    for _ in range(100):
        a = next_random()
        n = (a * 32768 + next_random()) % 999999 + 2
        want = min(next_random() % 100 + 1, n - 1)
        taken = set()
        cuts = []
        while len(cuts) < want:
            b = next_random()
            c = (b * 32768 + next_random()) % (n - 1) + 1
            if c not in taken:
                taken.add(c)
                cuts.append(c)
        sticks.append((n, cuts))
    check = 0
    for _ in range(4):
        for n, cuts in sticks:
            check = mix(check, min_cost(n, list(cuts)))
    print(f"4 passes over 100 sticks of up to 1000000 with up to 100 cuts: checksum {check}")


main()
