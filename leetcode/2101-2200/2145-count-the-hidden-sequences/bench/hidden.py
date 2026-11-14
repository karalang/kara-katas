# LeetCode #2145: Count the Hidden Sequences -- the benchmark, the same
# algorithm as hidden.kara.

seed = 2145


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def number_of_arrays(differences, lower, upper):
    at = lowest = highest = 0
    for d in differences:
        at += d
        if at < lowest:
            lowest = at
        if at > highest:
            highest = at
    return max(0, (upper - lower) - (highest - lowest) + 1)


def main():
    walks = [[next_random() % 21 - 10 for _ in range(100000)] for _ in range(20)]
    total = check = 0
    for rnd in range(200):
        for w in range(20):
            hi = next_random()
            at = (hi * 32768 + next_random()) % 100000
            walks[w][at] = next_random() % 21 - 10
            count = number_of_arrays(walks[w], -100000, 100000)
            total += count
            check = (check * 31 + count + rnd) % 1000000007
    print(f"4000 solves: {total} sequences in all, checksum {check}")


main()
