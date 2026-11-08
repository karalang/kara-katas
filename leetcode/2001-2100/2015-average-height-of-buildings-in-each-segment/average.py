# LeetCode #2015: Average Height of Buildings in Each Segment -- a mirror of
# the ★ arm, average.kara.


def average_height_of_buildings(buildings):
    events = []
    for start, end, height in buildings:
        events.append((start, height, 1))
        events.append((end, -height, -1))
    events.sort()
    street = []
    total = count = i = 0
    while i < len(events):
        at = events[i][0]
        while i < len(events) and events[i][0] == at:
            total += events[i][1]
            count += events[i][2]
            i += 1
        if count == 0:
            continue
        nxt = events[i][0]
        average = total // count
        if street and street[-1][1] == at and street[-1][2] == average:
            street[-1] = (street[-1][0], nxt, average)
        else:
            street.append((at, nxt, average))
    return street


seed = 2015


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, street):
    check = (check * 31 + len(street)) % 1000000007
    for left, right, average in street:
        check = (check * 31 + left) % 1000000007
        check = (check * 31 + right) % 1000000007
        check = (check * 31 + average) % 1000000007
    return check


def random_buildings(n, span, long, tall):
    buildings = []
    for _ in range(n):
        start = (next_random() * 32768 + next_random()) % span
        end = start + next_random() % long + 1
        buildings.append((start, end, next_random() % tall + 1))
    return buildings


def show(street):
    return "[" + ", ".join(f"({a}, {b}, {c})" for a, b, c in street) + "]"


def main():
    examples = [
        [(1, 4, 2), (3, 9, 4)],
        [(1, 3, 2), (2, 5, 3), (2, 8, 3)],
        [(1, 2, 1), (5, 6, 1)],
        [(0, 100000000, 100000)],
        [(1, 5, 4), (5, 9, 4)],
        [(1, 5, 4), (5, 9, 5), (3, 7, 1)],
        [(2, 6, 3), (2, 6, 5), (2, 6, 1)],
        [(4, 8, 2), (1, 3, 7), (3, 4, 7), (8, 9, 1), (6, 10, 1)],
    ]
    for buildings in examples:
        print(f"{show(buildings)} -> {show(average_height_of_buildings(buildings))}")
    segments = check = 0
    for _ in range(2000):
        n = next_random() % 12 + 1
        span = next_random() % 30 + 1
        long = next_random() % 10 + 1
        tall = next_random() % 6 + 1
        street = average_height_of_buildings(random_buildings(n, span, long, tall))
        segments += len(street)
        check = mix(check, street)
    print(f"2000 streets of 1 to 12 buildings: {segments} segments, checksum {check}")
    segments = check = 0
    for a in range(4):
        span = [1000, 100000, 99000000, 30000][a]
        long = [50, 1000, 1000000, 30000][a]
        tall = [3, 100000, 100, 2][a]
        street = average_height_of_buildings(random_buildings(2000, span, long, tall))
        segments += len(street)
        check = mix(check, street)
    print(f"4 streets of 2000 buildings: {segments} segments, checksum {check}")


main()
