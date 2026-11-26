# LeetCode #1467 Probability of a Two Boxes Having The Same Number of
# Distinct Balls: a mirror of get_probability.kara.


def choose(n, k):
    # n choose k, exactly
    c = 1
    for i in range(k):
        c = c * (n - i) // (i + 1)
    return c


def ways(balls, i, first, a, b):
    # the shuffles that put `first` balls into the first box and leave the
    # two boxes with as many colours each, over colours `i` onward, given
    # the colours each box holds so far
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
    # a shuffle is fixed by which places of the first half each ball
    # takes, so the balls of one colour split j to the first box in
    # C(n, j) ways; the wanted shuffles over all C(total, total / 2)
    total = sum(balls)
    good = ways(balls, 0, total // 2, 0, 0)
    return good / choose(total, total // 2)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw():
    while True:
        k = 1 + next_random() % 8
        balls = [1 + next_random() % 6 for _ in range(k)]
        if sum(balls) % 2 == 0:
            return balls


def main():
    global seed
    f = get_probability
    e = [f([1, 1]), f([2, 1, 1]), f([1, 2, 1, 2]), f([2]), f([3, 1]), f([6] * 8)]
    print(" ".join(repr(x) for x in e))
    seed = 1467
    total = 0.0
    check = 0
    for _ in range(300):
        p = f(draw())
        total += p
        check = (check * 31 + round(p * 1000000.0)) % 1000000007
    print(f"300 random sets: sum {total}, checksum {check}")


main()
