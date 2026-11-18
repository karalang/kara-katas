# LeetCode #2279: Maximum Bags With Full Capacity of Rocks -- the Python
# mirror of the ★ arm, `bags.kara`, line for line. Its output is
# byte-identical.


def maximum_bags(capacity, rocks, additional_rocks):
    lack = []
    for i in range(len(capacity)):
        lack.append(capacity[i] - rocks[i])
    lack.sort()
    left = additional_rocks
    full = 0
    for need in lack:
        if need > left:
            break
        left -= need
        full += 1
    return full


seed = 2279


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def bags(n, high):
    capacity = []
    rocks = []
    lack = 0
    for _ in range(n):
        c = wide_random() % high + 1
        if next_random() % 2 == 0:
            r = wide_random() % (c // 5 + 1)
        else:
            r = wide_random() % (c + 1)
        capacity.append(c)
        rocks.append(r)
        lack += c - r
    w = wide_random() % (lack + 1)
    spare = w // (next_random() % 4 + 1)
    return capacity, rocks, min(spare, 1000000000)


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    examples = [
        ([2, 3, 4, 5], [1, 2, 4, 4], 2),
        ([10, 2, 2], [2, 2, 0], 100),
        ([1], [1], 0),
        ([5], [0], 4),
        ([3, 3, 3], [0, 0, 0], 8),
        ([1, 1], [0, 0], 0),
        ([4, 4], [4, 4], 0),
    ]
    for capacity, rocks, spare in examples:
        print(f"{show(capacity)} {show(rocks)} {spare} -> {maximum_bags(capacity, rocks, spare)}")
    check = 0
    for t in range(2000):
        n = next_random() % 40 + 1
        capacity, rocks, spare = bags(n, [10, 1000, 1000000000][t % 3])
        check = (check * 31 + maximum_bags(capacity, rocks, spare)) % 1000000007
    print(f"2000 sets: checksum {check}")
    c1, r1, s1 = bags(50000, 1000000000)
    c2, r2, s2 = bags(50000, 100)
    ones = [1] * 50000
    empty = [0] * 50000
    answers = [maximum_bags(c1, r1, s1), maximum_bags(c2, r2, s2), maximum_bags(ones, empty, 1000000000)]
    print(f"5 * 10^4 bags: {show(answers)}")


main()
