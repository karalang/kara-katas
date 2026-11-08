# LeetCode #2021: Brightest Position on Street -- Python mirror of the ★ arm
# (brightest.kara). Two events per lamp, sorted; a sweep applies every event
# at a position before reading the brightness there.


def brightest_position(lights):
    events = []
    for position, range_ in lights:
        events.append((position - range_, 1))
        events.append((position + range_ + 1, -1))
    events.sort()
    brightness = best = answer = 0
    i = 0
    while i < len(events):
        at = events[i][0]
        while i < len(events) and events[i][0] == at:
            brightness += events[i][1]
            i += 1
        if brightness > best:
            best = brightness
            answer = at
    return answer


# ---- test harness ----------------------------------------------------------

seed = 2021


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_lights(count, spread, reach):
    lights = []
    for _ in range(count):
        position = next_random() % (2 * spread + 1) - spread
        lights.append((position, next_random() % (reach + 1)))
    return lights


def main():
    examples = [
        [(-3, 2), (1, 2), (3, 3)],
        [(1, 0), (0, 1)],
        [(1, 2)],
        [(5, 0)],
        [(0, 0), (0, 0), (10, 0)],
        [(-100000000, 100000000), (100000000, 100000000)],
        [(1, 1), (4, 1), (7, 1), (3, 0)],
        [(10, 5), (-10, 5), (0, 4)],
    ]
    for lights in examples:
        print(f"{lights} -> {brightest_position(lights)}")
    total = 0
    check = 0
    for _ in range(3000):
        count = next_random() % 12 + 1
        spread = next_random() % 20 + 1
        reach = next_random() % 8
        answer = brightest_position(random_lights(count, spread, reach))
        total += answer
        check = (check * 31 + answer + 1000) % 1000000007
    print(f"3000 streets of up to 12 lamps: sum {total}, checksum {check}")
    total = 0
    check = 0
    for a in range(5):
        spread = [100000000, 1000, 50000000, 10, 100000000][a]
        reach = [100000000, 50, 1000000, 3, 0][a]
        answer = brightest_position(random_lights(2000, spread, reach))
        total += answer
        check = (check * 31 + answer + 1000000000) % 1000000007
    print(f"5 streets of 2000 lamps: sum {total}, checksum {check}")


main()
