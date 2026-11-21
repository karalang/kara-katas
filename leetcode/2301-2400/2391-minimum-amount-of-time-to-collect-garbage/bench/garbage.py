# LeetCode #2391: Minimum Amount of Time to Collect Garbage -- the bench,
# the ★ arm in Python: the units counted once, each truck driven to the
# last house holding its kind by the travel's prefix sums.

seed = 2391


def garbage_collection(garbage, travel):
    minutes = 0
    last = [0, 0, 0]
    for i, house in enumerate(garbage):
        for c in house:
            minutes += 1
            last[0 if c == 77 else 1 if c == 80 else 2] = i
    prefix = [0]
    for t in travel:
        prefix.append(prefix[-1] + t)
    for kind in range(3):
        minutes += prefix[last[kind]]
    return minutes


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    streets = []
    roads = []
    for _ in range(50):
        street = []
        for _ in range(2000):
            length = 1 + next_random() % 10
            street.append(bytes(b"MPG"[next_random() % 3] for _ in range(length)))
        streets.append(street)
        roads.append([1 + next_random() % 100 for _ in range(1, 2000)])
    check = 0
    for p in range(500):
        for s in range(50):
            check = (check * 31 + garbage_collection(streets[s], roads[s]) + p) % 1000000007
    print(f"500 passes over 50 streets of 2000 houses: checksum {check}")


if __name__ == "__main__":
    main()
