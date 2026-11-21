# LeetCode #2466: Count Ways To Build Good Strings -- the bench, the ★ arm
# in Python: bottom-up counts, each length's the sum of the counts one
# block back, and the counts from `low` to `high` summed.

MOD = 1000000007


def count_good_strings(low, high, zero, one):
    ways = [0] * (high + 1)
    ways[0] = 1
    total = 0
    for length in range(1, high + 1):
        if length >= zero:
            ways[length] = (ways[length] + ways[length - zero]) % MOD
        if length >= one:
            ways[length] = (ways[length] + ways[length - one]) % MOD
        if length >= low:
            total = (total + ways[length]) % MOD
    return total


seed = 2466


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 cases built once, `high` from 50000 to 10^5, `low` from 1 to
    # `high`, blocks of 1 to 20 no longer than `low`; then 28 passes,
    # each setting every case's zero block from the checksum so far, then
    # answering it and folding the answer plus the pass into the checksum
    cases = []
    for _ in range(20):
        high = 50000 + (next_random() * 32768 + next_random()) % 50001
        low = 1 + (next_random() * 32768 + next_random()) % high
        zero = 1 + next_random() % min(low, 20)
        one = 1 + next_random() % min(low, 20)
        cases.append((low, high, zero, one))
    check = 0
    for p in range(28):
        for a in range(len(cases)):
            low, high, _, one = cases[a]
            zero = 1 + (check + a) % min(low, 20)
            cases[a] = (low, high, zero, one)
            check = (check * 31 + count_good_strings(low, high, zero, one) + p) % 1000000007
    print(f"28 passes over 20 cases up to 10^5: checksum {check}")


main()
