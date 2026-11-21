# LeetCode #2477: Minimum Fuel Cost to Report to the Capital -- the
# Python mirror of fuel.kara: a breadth-first order from the capital,
# walked backwards, gives each city its subtree's size, and the road out
# of it carries `ceil(size / seats)` cars.


def minimum_fuel_cost(roads, seats):
    n = len(roads) + 1
    adjacent = [[] for _ in range(n)]
    for a, b in roads:
        adjacent[a].append(b)
        adjacent[b].append(a)
    parent = [-1] * n
    order = [0]
    parent[0] = 0
    nxt = 0
    while nxt < len(order):
        city = order[nxt]
        nxt += 1
        for other in adjacent[city]:
            if parent[other] < 0:
                parent[other] = city
                order.append(other)
    size = [1] * n
    fuel = 0
    for k in range(n - 1, 0, -1):
        city = order[k]
        fuel += (size[city] + seats - 1) // seats
        size[parent[city]] += size[city]
    return fuel


# ---- test harness ---------------------------------------------------------

seed = 2477


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def random_roads(n):
    roads = []
    for k in range(1, n):
        other = wide_random() % k
        if next_random() % 2 == 0:
            roads.append([k, other])
        else:
            roads.append([other, k])
    for i in range(len(roads) - 1, 0, -1):
        j = wide_random() % (i + 1)
        roads[i], roads[j] = roads[j], roads[i]
    return roads


def show(v):
    return "[" + ", ".join(show(x) if isinstance(x, list) else str(x) for x in v) + "]"


def main():
    cases = [
        ([[0, 1], [0, 2], [0, 3]], 5),
        ([[3, 1], [3, 2], [1, 0], [0, 4], [0, 5], [4, 6]], 2),
        ([], 1),
        ([[0, 1], [1, 2], [2, 3], [3, 4]], 1),
        ([[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]], 2),
        ([[2, 1], [1, 0], [0, 3], [3, 4]], 3),
    ]
    for roads, seats in cases:
        print(f"{show(roads)}, seats {seats} -> {minimum_fuel_cost(roads, seats)}")
    big = random_roads(100000)
    for seats in [1, 3, 100000]:
        print(f"10^5 cities, seats {seats} -> {minimum_fuel_cost(big, seats)}")
    path = [[k - 1, k] for k in range(1, 2000)]
    print(f"a path of 2000, seats 1 -> {minimum_fuel_cost(path, 1)}")
    print(f"a path of 2000, seats 7 -> {minimum_fuel_cost(path, 7)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 40
        roads = random_roads(n)
        seats = 1 + next_random() % 10
        check = (check * 31 + minimum_fuel_cost(roads, seats)) % 1000000007
    print(f"3000 random: checksum {check}")


main()
