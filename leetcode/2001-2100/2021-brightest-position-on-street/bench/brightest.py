# LeetCode #2021: Brightest Position on Street -- the ★ arm's benchmark, a
# mirror of brightest.kara.


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


seed = 2021


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    streets = []
    for s in range(100):
        spread = [1000000, 10000000, 100000000][s % 3]
        reach = [1000, 100000, 1000000][s % 3]
        lights = []
        for _ in range(10000):
            hi = next_random()
            lo = next_random()
            position = (hi * 32768 + lo) % (2 * spread + 1) - spread
            lights.append((position, next_random() % (reach + 1)))
        streets.append(lights)
    calls = total = check = 0
    for _ in range(5):
        for lights in streets:
            answer = brightest_position(lights)
            calls += 1
            total += answer
            check = (check * 31 + answer + 1000000000) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
