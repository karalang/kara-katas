# Benchmark for #815: Bus Routes -- mirror of the ★ arm (breadth-first
# search over buses), with the same workload as bus_routes.kara.
from collections import deque


def num_buses_to_destination(routes, source, target):
    if source == target:
        return 0
    buses_at = {}
    for bus, route in enumerate(routes):
        for stop in route:
            buses_at.setdefault(stop, []).append(bus)
    if source not in buses_at:
        return -1
    taken = [False] * len(routes)
    queue = deque()
    for bus in buses_at[source]:
        taken[bus] = True
        queue.append((bus, 1))
    seen = set()
    while queue:
        bus, count = queue.popleft()
        for stop in routes[bus]:
            if stop == target:
                return count
            if stop in seen:
                continue
            seen.add(stop)
            for nxt in buses_at[stop]:
                if not taken[nxt]:
                    taken[nxt] = True
                    queue.append((nxt, count + 1))
    return -1


seed = 815


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 64, 4000
    cities = []
    for _ in range(count):
        routes = []
        for _ in range(100):
            length = 1 + next_random() % 200
            on = set()
            route = []
            while len(route) < length:
                stop = next_random() % 20000
                if stop not in on:
                    on.add(stop)
                    route.append(stop)
            routes.append(route)
        cities.append(routes)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        g = rnd % count
        ends = []
        for _ in range(2):
            if next_random() % 8 == 0:
                ends.append(next_random() % 20000)
            else:
                route = cities[g][next_random() % 100]
                ends.append(route[next_random() % len(route)])
        answer = num_buses_to_destination(cities[g], ends[0], ends[1])
        total += answer
        checksum = (checksum * 31 + answer + 2) % 1000000007
    print(f"{rounds} rounds of 100 routes: total {total}, checksum {checksum}")


main()
