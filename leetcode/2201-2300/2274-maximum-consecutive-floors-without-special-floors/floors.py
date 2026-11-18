# LeetCode #2274: Maximum Consecutive Floors Without Special Floors --
# the Python mirror of the ★ arm, `floors.kara`, line for line. Its
# output is byte-identical.


def max_consecutive(bottom, top, special):
    floors = sorted(special)
    best = max(floors[0] - bottom, top - floors[-1])
    for i in range(1, len(floors)):
        best = max(best, floors[i] - floors[i - 1] - 1)
    return best


seed = 2274


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def floors(bottom, top, k, gap):
    special = []
    f = bottom + next_random() % min(gap, top - bottom + 1)
    while f <= top and len(special) < k:
        special.append(f)
        f += 1 + next_random() % gap
    for j in range(len(special) - 1, 0, -1):
        r = next_random() % (j + 1)
        special[j], special[r] = special[r], special[j]
    return special


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    examples = [
        (2, 9, [4, 6]),
        (6, 8, [7, 6, 8]),
        (1, 1, [1]),
        (1, 10, [5]),
        (1, 10, [1, 10]),
        (1, 10, [10]),
        (3, 20, [15, 3, 5, 4]),
    ]
    for bottom, top, special in examples:
        print(f"{bottom}..{top} {show(special)} -> {max_consecutive(bottom, top, special)}")
    check = 0
    for t in range(2000):
        bottom = next_random() % 100 + 1
        span = [10, 100, 10000, 1000000000][t % 4]
        top = min(bottom + next_random() % span, 1000000000)
        k = next_random() % 20 + 1
        special = floors(bottom, top, k, [3, 50, 1000000][t // 4 % 3])
        check = (check * 31 + max_consecutive(bottom, top, special)) % 1000000007
    print(f"2000 buildings: checksum {check}")
    rand = floors(1, 1000000000, 100000, 20000)
    every = list(range(1, 100001))
    third = [3 * i for i in range(1, 100001)]
    answers = [
        max_consecutive(1, 1000000000, rand),
        max_consecutive(1, 100000, every),
        max_consecutive(1, 300000, third),
    ]
    print(f"10^5 specials: {show(answers)}")


main()
