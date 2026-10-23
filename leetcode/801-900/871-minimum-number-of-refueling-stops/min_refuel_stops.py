# LeetCode #871: Minimum Number of Refueling Stops -- a heap of the
# stations passed; a mirror of min_refuel_stops.kara, its output
# byte-identical.

import heapq


def min_refuel_stops(target, start_fuel, stations):
    passed = []
    reach = start_fuel
    stops = 0
    nxt = 0
    while reach < target:
        while nxt < len(stations) and stations[nxt][0] <= reach:
            heapq.heappush(passed, -stations[nxt][1])
            nxt += 1
        if not passed:
            return -1
        reach += -heapq.heappop(passed)
        stops += 1
    return stops


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_below(limit):
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % limit


def random_stations(n, target, max_fuel):
    positions = []
    if target > 1:
        for _ in range(n):
            positions.append(random_below(target - 1) + 1)
    positions = sorted(set(positions))
    return [(p, random_below(max_fuel) + 1) for p in positions]


def show(target, start_fuel, stations):
    listed = ", ".join(f"[{p}, {f}]" for p, f in stations)
    print(f"target = {target}, startFuel = {start_fuel}, stations = [{listed}] -> {min_refuel_stops(target, start_fuel, stations)}")


def main():
    global seed
    show(1, 1, [])
    show(100, 1, [(10, 100)])
    show(100, 10, [(10, 60), (20, 30), (30, 30), (60, 40)])
    show(100, 100, [])
    show(100, 99, [])
    show(100, 50, [(50, 50)])
    show(100, 49, [(50, 50)])
    show(100, 10, [(10, 10), (20, 10), (30, 10), (40, 10), (50, 10), (60, 10), (70, 10), (80, 10), (90, 10)])
    show(100, 25, [(25, 25), (50, 25), (75, 25), (80, 1000)])
    show(1000000000, 1, [(1, 999999999)])
    show(1000000000, 1000000000, [(1, 999999999)])
    show(1000000000, 1, [(2, 999999999)])
    seed = 871
    total = 0
    unreachable = 0
    for k in range(3000):
        target = random_below(100) + 1
        start_fuel = random_below(target + 10) + 1
        stations = random_stations(k % 9, target, 40)
        a = min_refuel_stops(target, start_fuel, stations)
        if a < 0:
            unreachable += 1
        else:
            total += a
    print(f"3000 cases with a target up to 100: stops sum to {total}, {unreachable} unreachable")
    total = 0
    unreachable = 0
    check = 0
    for k in range(40):
        target = random_below(1000000000) + 1
        start_fuel = random_below(target // 50 + 1) + 1
        max_fuel = target // 20 + 1 if k % 2 == 0 else target // 100 + 1
        stations = random_stations(500, target, max_fuel)
        a = min_refuel_stops(target, start_fuel, stations)
        if a < 0:
            unreachable += 1
        else:
            total += a
        check = (check * 1009 + a + 1) % 1000000007
    print(f"40 cases with 500 stations: stops sum to {total}, {unreachable} unreachable, checksum {check}")


main()
