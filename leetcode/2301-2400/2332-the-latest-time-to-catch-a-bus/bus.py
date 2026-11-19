# LeetCode #2332: The Latest Time to Catch a Bus -- the Python mirror of
# the ★ arm: both lists sorted and the buses filled in order; the last
# bus's departure if it leaves with room, else its last passenger's
# time, then a step back past every passenger standing at the time tried.


def latest_time_catch_the_bus(buses, passengers, capacity):
    buses = sorted(buses)
    passengers = sorted(passengers)
    nxt = 0
    aboard = 0
    for bus in buses:
        aboard = 0
        while aboard < capacity and nxt < len(passengers) and passengers[nxt] <= bus:
            aboard += 1
            nxt += 1
    latest = buses[-1] if aboard < capacity else passengers[nxt - 1]
    k = nxt - 1
    while k >= 0 and passengers[k] == latest:
        latest -= 1
        k -= 1
    return latest


seed = 2332


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def distinct_times(count, top):
    taken = set()
    times = []
    while len(times) < count:
        t = next_random() % (top - 1) + 2
        if t not in taken:
            taken.add(t)
            times.append(t)
    return times


def main():
    print(latest_time_catch_the_bus([10, 20], [2, 17, 18, 19], 2))
    print(latest_time_catch_the_bus([20, 30, 10], [19, 13, 26, 4, 25, 11, 21], 2))
    print(latest_time_catch_the_bus([5], [5], 1))
    print(latest_time_catch_the_bus([10, 20], [2, 3, 4, 5, 6], 2))
    print(latest_time_catch_the_bus([9], list(range(2, 10)), 10))
    buses = distinct_times(1000, 1000000000)
    passengers = distinct_times(2000, 1000000000)
    print(latest_time_catch_the_bus(buses, passengers, 3))
    check = 0
    total = 0
    for _ in range(2000):
        n = next_random() % 8 + 1
        m = next_random() % 12 + 1
        capacity = next_random() % 3 + 1
        buses = distinct_times(n, 40)
        passengers = distinct_times(m, 40)
        latest = latest_time_catch_the_bus(buses, passengers, capacity)
        check = (check * 31 + latest) % 1000000007
        total += latest
    print(f"2000 cases: checksum {check}, total {total}")


main()
