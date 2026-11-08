# LeetCode #2008: Maximum Earnings From Taxi -- the ★ arm's benchmark, a
# mirror of taxi.kara.


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


def main():
    roads = []
    for _ in range(80):
        rides = []
        for _ in range(5000):
            length = next_random() % 100 + 1
            start = next_random() % (9900 - length) + 1
            rides.append((start, start + length, next_random() % 1001))
        roads.append(rides)
    calls = 0
    total = 0
    check = 0
    for r in range(25):
        for a in range(len(roads)):
            answer = max_taxi_earnings(10000 - r * 4, roads[a])
            calls += 1
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
