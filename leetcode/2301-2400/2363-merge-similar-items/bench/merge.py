# LeetCode #2363: Merge Similar Items -- the bench, the ★ arm in Python:
# every item of both lists added into a sorted map from value to total
# weight, which walks out in order of value. Python has no sorted map, so
# the values are kept as a sorted list by `bisect` beside a dict of
# totals.

from bisect import insort


def merge_similar_items(items1, items2):
    keys = []
    totals = {}
    for value, weight in items1 + items2:
        if value in totals:
            totals[value] += weight
        else:
            insort(keys, value)
            totals[value] = weight
    return [[value, totals[value]] for value in keys]


SEED = [2363]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def random_items(count):
    # count distinct values from 1 to 1000 in a shuffled order, each with
    # a weight of 1 to 1000
    values = list(range(1, 1001))
    for i in range(999, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    return [[values[i], 1 + next_random() % 1000] for i in range(count)]


def main():
    # pair a: lists of 100 (a + 1) and 1000 - 50 a items
    pairs = []
    for a in range(10):
        items1 = random_items(100 * (a + 1))
        items2 = random_items(1000 - 50 * a)
        pairs.append((items1, items2))
    check = 0
    for p in range(400):
        for items1, items2 in pairs:
            merged = merge_similar_items(items1, items2)
            check = (check * 31 + len(merged) * 1009 + merged[-1][1] + p) % 1000000007
    print(f"400 passes over 10 pairs of lists: checksum {check}")


main()
