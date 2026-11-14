# LeetCode #2145: Count the Hidden Sequences -- the Python mirror of
# hidden.kara's ★ arm.


def number_of_arrays(differences, lower, upper):
    at = 0
    lowest = 0
    highest = 0
    for d in differences:
        at += d
        lowest = min(lowest, at)
        highest = max(highest, at)
    return max(0, (upper - lower) - (highest - lowest) + 1)


seed = 2145


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(differences, lower, upper):
    print(f"[{', '.join(map(str, differences))}] {lower} {upper} -> {number_of_arrays(differences, lower, upper)}")


def main():
    show([1, -3, 4], 1, 6)
    show([3, -4, 5, 1, -2], -4, 5)
    show([4, -7, 2], 3, 6)
    show([0], 5, 5)
    show([100000], -100000, 100000)
    show([5], 0, 4)
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 12 + 1
        top = [5, 10000][rnd % 2]
        differences = [next_random() % (2 * top + 1) - top for _ in range(n)]
        a = next_random() % (20 * top + 1) - 10 * top
        b = next_random() % (20 * top + 1) - 10 * top
        lower = min(a, b)
        upper = max(a, b)
        count = number_of_arrays(differences, lower, upper)
        total += count
        check = (check * 31 + count + n) % 1000000007
    print(f"2000 walks: {total} sequences in all, checksum {check}")
    ones = [1] * 100000
    swings = [100000 if i % 2 == 0 else -100000 for i in range(100000)]
    rand = [(next_random() * 32768 + next_random()) % 21 - 10 for _ in range(100000)]
    x = number_of_arrays(ones, -100000, 100000)
    y = number_of_arrays(swings, -100000, 100000)
    z = number_of_arrays(rand, -100000, 100000)
    print(f"100000 differences: {x} all 1, {y} swinging, {z} at random")


main()
