# LeetCode #2367: Number of Arithmetic Triplets -- the bench, the ★ arm in
# Python: a set of the values, and each value x the start of a triplet
# when the set holds x + diff and x + 2 diff.


def arithmetic_triplets(nums, diff):
    values = set(nums)
    count = 0
    for x in nums:
        if x + diff in values and x + 2 * diff in values:
            count += 1
    return count


SEED = [2367]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # set s: each value from 0 to 200 kept with a chance of 1 + s % 8 in 8,
    # and at least the three values 0, 1 and 2
    sets = []
    for s in range(1000):
        sets.append([v for v in range(201) if v < 3 or next_random() % 8 <= s % 8])
    check = 0
    for p in range(50):
        for s in range(1000):
            diff = 1 + (s + p) % 50
            check = (check * 31 + arithmetic_triplets(sets[s], diff) + p) % 1000000007
    print(f"50 passes over 1000 sets of up to 201 values: checksum {check}")


main()
