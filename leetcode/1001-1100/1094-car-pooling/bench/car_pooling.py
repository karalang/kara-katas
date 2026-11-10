# Benchmark: LeetCode #1094 Car Pooling -- the ★ arm, a difference array
# over the stops. Mirrors car_pooling.kara.


def car_pooling(trips, capacity):
    change = [0] * 1001
    for t in trips:
        change[t[1]] += t[0]
        change[t[2]] -= t[0]
    aboard = 0
    for c in change:
        aboard += c
        if aboard > capacity:
            return False
    return True


seed = 1094


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    for _ in range(64):
        trips = []
        for _ in range(1000):
            n = next_random() % 100 + 1
            a = next_random() % 1000
            b = a + 1 + next_random() % (1000 - a)
            trips.append([n, a, b])
        lists.append(trips)
    total = 0
    check = 0
    for rnd in range(100):
        for j in range(len(lists)):
            k = (rnd * 7 + j * 13) % 1000
            lists[j][k][0] = 1 + (lists[j][k][0] + rnd) % 100
            lo, hi = 1, 100000
            while lo < hi:
                mid = (lo + hi) // 2
                if car_pooling(lists[j], mid):
                    hi = mid
                else:
                    lo = mid + 1
            total += lo
            check = (check * 31 + lo) % 1000000007
    print(f"100 rounds over 64 lists of 1000 trips: smallest capacities sum to {total}, checksum {check}")


main()
