# LeetCode #1547: Minimum Cost to Cut a Stick -- Python mirror of cut.kara
# (the ★ arm, interval DP over the sorted points); its output is
# byte-identical.


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


def batch(count, longest, most):
    check = 0
    for _ in range(count):
        a = next_random()
        n = (a * 32768 + next_random()) % (longest - 1) + 2
        want = min(next_random() % most + 1, n - 1)
        taken = set()
        cuts = []
        while len(cuts) < want:
            a = next_random()
            c = (a * 32768 + next_random()) % (n - 1) + 1
            if c not in taken:
                taken.add(c)
                cuts.append(c)
        check = mix(check, min_cost(n, cuts))
    print(f"{count} sticks of up to {longest} with up to {most} cuts: checksum {check}")


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        (7, [1, 3, 4, 5]),
        (9, [5, 6, 1, 4, 2]),
        (2, [1]),
        (10, [5]),
        (10, [1, 9]),
        (1000000, [1, 999999, 500000]),
    ]
    for n, cuts in examples:
        print(f"n = {n}, cuts {show(cuts)} -> {min_cost(n, cuts)}")
    print(f"n = 101, every cut -> {min_cost(101, list(range(1, 101)))}")
    batch(3000, 30, 6)
    batch(300, 1000000, 40)
    batch(3, 1000000, 100)


main()
