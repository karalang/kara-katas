# LeetCode #2187: Minimum Time to Complete Trips -- the Python mirror of
# trips.kara: a binary search over the time, the trips by each time
# counted until they reach the total.


def trips_by(time, t, total_trips):
    trips = 0
    for x in time:
        trips += t // x
        if trips >= total_trips:
            break
    return trips


def minimum_time(time, total_trips):
    fastest = time[0]
    for x in time:
        fastest = min(fastest, x)
    lo = 1
    hi = fastest * total_trips
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if trips_by(time, mid, total_trips) >= total_trips:
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---- test harness ---------------------------------------------------------

seed = 2187


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(time, total_trips):
    print(f"[{', '.join(str(x) for x in time)}], {total_trips} -> {minimum_time(time, total_trips)}")


def main():
    show([1, 2, 3], 5)
    show([2], 1)
    show([10000000], 10000000)
    show([3, 3, 3], 7)
    show([1, 1000], 4)
    show([2, 3, 4], 7)
    total = 0
    check = 0
    for rnd in range(2000):
        big = rnd % 2 == 1
        n = next_random() % 20 + 1
        time = []
        for _ in range(n):
            if big:
                t = (next_random() * 32768 + next_random()) % 10000000 + 1
            else:
                t = next_random() % 10 + 1
            time.append(t)
        if big:
            trips = (next_random() * 32768 + next_random()) % 10000000 + 1
        else:
            trips = next_random() % 100 + 1
        answer = minimum_time(time, trips)
        total = (total + answer) % 1000000007
        check = (check * 31 + answer % 1000000007 + n) % 1000000007
    print(f"2000 fleets: {total} in all, checksum {check}")
    slow = [10000000] * 100000
    fast = [1] * 100000
    mixed = []
    for _ in range(100000):
        mixed.append((next_random() * 32768 + next_random()) % 10000000 + 1)
    print(f"10^5 buses: {minimum_time(slow, 10000000)} {minimum_time(fast, 10000000)} {minimum_time(mixed, 10000000)}")


main()
