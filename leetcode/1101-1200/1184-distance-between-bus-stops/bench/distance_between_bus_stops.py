# LeetCode #1184: Distance Between Bus Stops -- the ★ arm in Python: the
# arc from the lower stop to the higher, against the whole ring less it.


def distance_between_bus_stops(distance, start, destination):
    lo, hi = min(start, destination), max(start, destination)
    total = sum(distance)
    one_way = sum(distance[lo:hi])
    return min(one_way, total - one_way)


def main():
    seed = 1184

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    rings, pairs = [], []
    for _ in range(50):
        rings.append([next_random() % 10001 for _ in range(10000)])
        for _ in range(200):
            start = next_random() % 10000
            destination = next_random() % 10000
            pairs.append((start, destination))
    rounds = 10
    check = 0
    for rnd in range(rounds):
        for r, ring in enumerate(rings):
            for k in range(200):
                start, destination = pairs[r * 200 + k]
                check = (check * 131 + distance_between_bus_stops(ring, start, destination) + rnd) % 1000000007
    print(f"{rounds} rounds of 10000 queries over 50 rings: checksum {check}")


main()
