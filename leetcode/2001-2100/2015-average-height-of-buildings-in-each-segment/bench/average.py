# LeetCode #2015: Average Height of Buildings in Each Segment -- the ★ arm's
# benchmark, a mirror of average.kara.


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


def main():
    streets = []
    for s in range(60):
        buildings = []
        for _ in range(10000):
            start = (next_random() * 32768 + next_random()) % 1000000
            end = start + next_random() % (100 * (s + 1)) + 1
            buildings.append((start, end, next_random() % (s + 2) + 1))
        streets.append(buildings)
    calls = segments = check = 0
    for _ in range(5):
        for buildings in streets:
            street = average_height_of_buildings(buildings)
            calls += 1
            segments += len(street)
            for left, right, average in street:
                check = (check * 31 + left + right * 7 + average * 13) % 1000000007
    print(f"{calls} calls: {segments} segments, checksum {check}")


main()
