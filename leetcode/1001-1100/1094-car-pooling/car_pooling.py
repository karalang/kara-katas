# LeetCode #1094: Car Pooling -- Python mirror of the ★ arm: the change in
# passengers aboard at each stop, summed from stop 0 on. Same cases and
# output as car_pooling.kara.


def car_pooling(trips, capacity):
    change = [0] * 1001
    for n, a, b in trips:
        change[a] += n
        change[b] -= n
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


def smallest_capacity(trips, most):
    lo, hi = 1, most
    while lo < hi:
        mid = (lo + hi) // 2
        if car_pooling(trips, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def show(b):
    return "true" if b else "false"


cases = [
    ([[2, 1, 5], [3, 3, 7]], 4),
    ([[2, 1, 5], [3, 3, 7]], 5),
    ([[2, 1, 5], [3, 5, 7]], 3),
    ([[3, 2, 7], [3, 7, 9], [8, 3, 9]], 11),
    ([[3, 2, 7], [3, 7, 9], [8, 3, 9]], 10),
    ([[5, 0, 1]], 4),
    ([[5, 0, 1]], 5),
    ([[1, 0, 1000]], 1),
    ([[100, 999, 1000], [100, 0, 999]], 100),
    ([[2, 0, 3], [2, 1, 4], [2, 2, 5], [2, 3, 6]], 6),
    ([[2, 0, 3], [2, 1, 4], [2, 2, 5], [2, 3, 6]], 5),
    ([[4, 5, 6], [4, 5, 6], [4, 5, 6]], 12),
]
for trips, capacity in cases:
    print(show(car_pooling(trips, capacity)))
total = enough = check = 0
for _ in range(2000):
    trips = []
    for _ in range(next_random() % 12 + 1):
        n = next_random() % 10 + 1
        a = next_random() % 21
        b = next_random() % 21
        while b == a:
            b = next_random() % 21
        trips.append([n, min(a, b), max(a, b)])
    capacity = next_random() % 40 + 1
    least = smallest_capacity(trips, 120)
    total += least
    if car_pooling(trips, capacity):
        enough += 1
    check = (check * 31 + least) % 1000000007
print(f"2000 random trip lists: smallest capacities sum to {total}, {enough} with enough seats, checksum {check}")
trips = []
for _ in range(1000):
    n = next_random() % 100 + 1
    a = next_random() % 1000
    b = a + 1 + next_random() % (1000 - a)
    trips.append([n, a, b])
least = smallest_capacity(trips, 100000)
print(f"1000 trips: smallest capacity {least}, {show(car_pooling(trips, least))} at it, {show(car_pooling(trips, least - 1))} one below")
