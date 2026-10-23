# LeetCode #926: Flip String to Monotone Increasing -- bench: one pass.
# Mirrors min_flips_mono_incr.kara.


def min_flips_mono_incr(s):
    flips = 0
    ones = 0
    for c in s:
        if c == "1":
            ones += 1
        else:
            flips = min(flips + 1, ones)
    return flips


seed = 926


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 20, 100, 100000
    # count strings of n characters, built once, leaning from 0 to 1
    strings = []
    for i in range(count):
        lean = i % 101
        strings.append("".join("1" if next_random() % 100 < lean else "0" for _ in range(n)))
    total = 0
    check = 0
    for r in range(rounds):
        # each round visits every string, starting from a different one
        for i in range(count):
            a = min_flips_mono_incr(strings[(r + i) % count])
            total += a
            check = (check * 1000003 + a) % 1000000007
    print(f"{rounds} rounds over {count} strings of {n}: answers summing to {total}, checksum {check}")


main()
