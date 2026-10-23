# LeetCode #871: Minimum Number of Refueling Stops -- Python mirror of the
# bench program (the ★ arm, a heap of the stations passed).

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


seed = 871


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_below(limit):
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % limit


def main():
    total = 0
    unreachable = 0
    check = 0
    for _ in range(100):
        target = random_below(500000000) + 500000001
        positions = sorted(set(random_below(target - 1) + 1 for _ in range(500)))
        stations = [(p, random_below(target // 40) + 1) for p in positions]
        for j in range(400):
            a = min_refuel_stops(target, j * (target // 800) + 1, stations)
            if a < 0:
                unreachable += 1
            else:
                total += a
            check = (check * 31 + a + 1) % 1000000007
    print(f"40000 trips over 100 lists of 500 stations: stops sum to {total}, {unreachable} unreachable, checksum {check}")


main()
