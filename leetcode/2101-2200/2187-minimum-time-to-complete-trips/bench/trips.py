# LeetCode #2187: Minimum Time to Complete Trips -- the benchmark's
# Python mirror of trips.kara: a binary search over the time with the
# count cut at the total.


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


seed = 2187


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    a = next_random()
    b = next_random()
    return a * 32768 + b


def main():
    row = [big_random() % 10000000 + 1 for _ in range(1000000)]
    check = 0
    for _ in range(200):
        start = big_random() % 900001
        trips = big_random() % 10000000 + 1
        t = minimum_time(row[start:start + 100000], trips)
        check = (check * 31 + t % 1000000007) % 1000000007
    print(f"200 solves: checksum {check}")


main()
