# LeetCode #2279: Maximum Bags With Full Capacity of Rocks -- the bench,
# the ★ arm.


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


# ---- bench harness ---------------------------------------------------------

seed = 2279


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(high):
    top = next_random()
    return (top * 32768 + next_random()) % high


def main():
    check = 0
    for _ in range(50):
        capacity = []
        rocks = []
        for _ in range(50000):
            c = draw(1000000000) + 1
            capacity.append(c)
            rocks.append(draw(c + 1))
        spare = draw(1000000000) + 1
        check = (check * 31 + maximum_bags(capacity, rocks, spare)) % 1000000007
    print(f"50 sets of 5 * 10^4: checksum {check}")


main()
