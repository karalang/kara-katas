# LeetCode #2237: Count Positions on Street With Required Brightness --
# the mirror of brightness.kara: a difference array over the street, a
# running sum, and the positions meeting their requirement counted.


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


def text(values):
    return "[" + ", ".join(text(v) if isinstance(v, list) else str(v) for v in values) + "]"


def show(n, lights, requirement):
    print(f"n = {n}, lights {text(lights)}, requirement {text(requirement)} -> {meet_requirement(n, lights, requirement)}")


def main():
    show(5, [[0, 1], [2, 1], [3, 2]], [0, 2, 1, 4, 1])
    show(1, [[0, 1]], [2])
    show(4, [[1, 0]], [0, 0, 0, 0])
    show(3, [[1, 100000]], [1, 1, 1])
    show(3, [[1, 1], [1, 1]], [2, 2, 2])
    show(4, [[0, 0], [3, 0]], [1, 0, 0, 1])
    show(3, [[0, 2], [2, 0]], [2, 2, 3])
    check = 0
    for c in range(3000):
        n = next_random() % 30 + 1
        m = next_random() % 30 + 1
        lights = []
        for _ in range(m):
            position = next_random() % n
            rng = wide_random() % 100001 if c % 10 == 0 else next_random() % (n + 1)
            lights.append([position, rng])
        requirement = [next_random() % (m + 1) for _ in range(n)]
        check = (check * 31 + meet_requirement(n, lights, requirement)) % 1000000007
    print(f"3000 streets: checksum {check}")
    for top in [100000, 100]:
        n = 100000
        lights = []
        for _ in range(100000):
            position = wide_random() % n
            lights.append([position, wide_random() % (top + 1)])
        requirement = [wide_random() % (top + 1) for _ in range(n)]
        print(f"10^5 positions and lights, ranges and requirements up to {top}: {meet_requirement(n, lights, requirement)}")


main()
