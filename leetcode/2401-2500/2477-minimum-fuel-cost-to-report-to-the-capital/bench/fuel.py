# LeetCode #2477: Minimum Fuel Cost to Report to the Capital -- the bench,
# the ★ arm in Python: a breadth-first order from the capital, walked
# backwards, gives each city its subtree's size, and the road out of it
# carries `ceil(size / seats)` cars.


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


def main():
    # 20 random trees of 10^4 cities built once; then 60 passes, each
    # answering every tree with 1 to 50 seats chosen by the checksum so
    # far, folding the fuel plus the pass into the checksum
    trees = [random_roads(10000) for _ in range(20)]
    check = 0
    for p in range(60):
        for roads in trees:
            seats = 1 + check % 50
            check = (check * 31 + minimum_fuel_cost(roads, seats) + p) % 1000000007
    print(f"60 passes over 20 trees of 10^4: checksum {check}")


main()
