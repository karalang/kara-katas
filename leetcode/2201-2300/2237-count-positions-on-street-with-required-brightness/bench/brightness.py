# LeetCode #2237: Count Positions on Street With Required Brightness --
# the benchmark's Python mirror of brightness.kara: a difference array,
# a running sum, and the positions meeting their requirement counted.


def meet_requirement(n, lights, requirement):
    change = [0] * (n + 1)
    for position, rng in lights:
        change[max(position - rng, 0)] += 1
        change[min(position + rng, n - 1) + 1] -= 1
    brightness = 0
    count = 0
    for i in range(n):
        brightness += change[i]
        if brightness >= requirement[i]:
            count += 1
    return count


seed = 2237


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    n = 100000
    lights = []
    for _ in range(100000):
        position = wide_random() % n
        lights.append((position, wide_random() % 1001))
    requirement = [wide_random() % 2001 for _ in range(n)]
    check = 0
    for _ in range(100):
        # punch: one light and one requirement drawn again before each pass
        at = wide_random() % 100000
        position = wide_random() % n
        lights[at] = (position, wide_random() % 1001)
        where = wide_random() % n
        requirement[where] = wide_random() % 2001
        check = (check * 31 + meet_requirement(n, lights, requirement)) % 1000000007
    print(f"100 passes over 10^5 positions and lights: checksum {check}")


main()
