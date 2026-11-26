# LeetCode #1467 bench in Python: the ★ arm (a depth-first search over how
# many of each colour go into the first box) on the same 100 sets of 8
# colours and 2 passes.

import math


def choose(n, k):
    c = 1
    for i in range(k):
        c = c * (n - i) // (i + 1)
    return c


def ways(balls, i, first, a, b):
    if i == len(balls):
        return 1 if first == 0 and a == b else 0
    n = balls[i]
    total = 0
    for j in range(min(n, first) + 1):
        a2 = a + 1 if j > 0 else a
        b2 = b + 1 if j < n else b
        total += choose(n, j) * ways(balls, i + 1, first - j, a2, b2)
    return total


def get_probability(balls):
    total = sum(balls)
    good = ways(balls, 0, total // 2, 0, 0)
    return good / choose(total, total // 2)


seed = 1467


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    sets = []
    while len(sets) < 100:
        balls = [1 + next_random() % 6 for _ in range(8)]
        if sum(balls) % 2 == 0:
            sets.append(balls)
    check = 0
    for pass_ in range(2):
        for s in range(100):
            k = check % 8
            sets[s][k] = sets[s][k] + 2 if sets[s][k] <= 4 else sets[s][k] - 2
            p = get_probability(sets[s])
            check = (check * 31 + math.floor(p * 1000000000.0 + 0.5) + pass_) % 1000000007
    print(f"2 passes over 100 sets of 8 colours: checksum {check}")


main()
