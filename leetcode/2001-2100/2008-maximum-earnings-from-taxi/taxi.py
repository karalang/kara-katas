# LeetCode #2008: Maximum Earnings From Taxi -- the mirror of the ★ arm,
# taxi.kara; its output is byte-identical.


def max_taxi_earnings(n, rides):
    ending = [[] for _ in range(n + 1)]
    for start, end, tip in rides:
        ending[end].append((start, end - start + tip))
    best = [0] * (n + 1)
    for p in range(2, n + 1):
        best[p] = best[p - 1]
        for start, earned in ending[p]:
            best[p] = max(best[p], best[start] + earned)
    return best[n]


seed = 2008


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


# `m` rides on a road of `n` points, each at most `span` long, tips up to `tip`
def random_rides(n, m, span, tip):
    rides = []
    for _ in range(m):
        length = next_random() % min(span, n - 1) + 1
        start = next_random() % (n - length) + 1
        rides.append((start, start + length, next_random() % (tip + 1)))
    return rides


def show(rides):
    return "[" + ", ".join(f"({s}, {e}, {t})" for s, e, t in rides) + "]"


def main():
    # LeetCode's two examples, then a few more
    examples = [
        (5, [(2, 5, 4), (1, 5, 1)]),
        (20, [(1, 6, 1), (3, 10, 2), (10, 12, 3), (11, 12, 2), (12, 15, 2), (13, 18, 1)]),
        (2, [(1, 2, 0)]),
        (10, [(1, 10, 0), (1, 5, 3), (5, 10, 3)]),
        (10, [(2, 3, 5), (2, 3, 7), (3, 4, 0)]),
        (6, [(1, 3, 0), (3, 6, 0), (1, 6, 1)]),
    ]
    for n, rides in examples:
        print(f"n = {n} {show(rides)} -> {max_taxi_earnings(n, rides)}")
    total = check = 0
    for _ in range(3000):
        n = next_random() % 15 + 2
        m = next_random() % 8 + 1
        span = next_random() % 6 + 1
        tip = next_random() % 5
        answer = max_taxi_earnings(n, random_rides(n, m, span, tip))
        total += answer
        check = mix(check, answer)
    print(f"3000 roads of 2 to 16 points: sum {total}, checksum {check}")
    total = check = 0
    for a in range(6):
        n = [1000, 100000][a % 2]
        span = [3, 50, 1000][a % 3]
        answer = max_taxi_earnings(n, random_rides(n, 30000, span, 100000))
        total += answer
        check = mix(check, answer)
    print(f"6 roads of 30000 rides: sum {total}, checksum {check}")


main()
