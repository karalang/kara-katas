# LeetCode #1184: Distance Between Bus Stops -- the ★ arm in Python: the arc
# from the lower stop to the higher, against the ring less it. Also checks
# the answer against the statement read literally (ride the bus each way
# round, stop by stop) on every random ring.


def distance_between_bus_stops(distance, start, destination):
    lo, hi = min(start, destination), max(start, destination)
    total = sum(distance)
    one_way = sum(distance[lo:hi])
    return min(one_way, total - one_way)


def literal(distance, start, destination):
    n = len(distance)
    best = None
    for step in (1, -1):
        at, ridden = start, 0
        while at != destination:
            if step == 1:
                ridden += distance[at]
                at = (at + 1) % n
            else:
                at = (at - 1) % n
                ridden += distance[at]
        best = ridden if best is None else min(best, ridden)
    return best


seed = 1184


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(name, distance, start, destination):
    got = distance_between_bus_stops(distance, start, destination)
    assert got == literal(distance, start, destination)
    print(f"{name}: {got}")


show("example 1", [1, 2, 3, 4], 0, 1)
show("example 2", [1, 2, 3, 4], 0, 2)
show("example 3", [1, 2, 3, 4], 0, 3)
show("small 1", [7], 0, 0)
show("small 2", [5, 9], 1, 0)
show("small 3", [3, 0, 0, 3], 3, 1)
show("small 4", [7, 10, 1, 12, 11, 14, 5, 0], 7, 2)
checksum = 0
for t in range(3000):
    n = 1 + next_random() % 12
    distance = [next_random() % 21 for _ in range(n)]
    start = next_random() % n
    destination = next_random() % n
    got = distance_between_bus_stops(distance, start, destination)
    assert got == literal(distance, start, destination), (distance, start, destination)
    checksum = (checksum * 31 + got + t) % 1000000007
print(f"3000 random rings: checksum {checksum}")
ring = [next_random() % 10001 for _ in range(10000)]
show("10000 stops", ring, 1234, 8765)
