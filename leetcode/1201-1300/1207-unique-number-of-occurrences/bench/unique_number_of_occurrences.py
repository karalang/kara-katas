# LeetCode #1207 bench, in Python: the ★ arm (each value's count in a dict,
# and the counts put in a set) on 2000 arrays of 1000 values drawn once,
# then 10 rounds over the arrays, how many answer true folded into a
# checksum.

seed = 1207


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def unique_occurrences(arr):
    counts = {}
    for v in arr:
        counts[v] = counts.get(v, 0) + 1
    return len(set(counts.values())) == len(counts)


def pick(values, total):
    r = next_random() % total
    j = 0
    while r > j:
        r -= j + 1
        j += 1
    return values[j]


def main():
    arrays = []
    for _ in range(2000):
        k = next_random() % 12 + 1
        values = [next_random() % 2001 - 1000 for _ in range(k)]
        total = k * (k + 1) // 2
        arrays.append([pick(values, total) for _ in range(1000)])
    check = 0
    for rnd in range(10):
        yes = sum(1 for arr in arrays if unique_occurrences(arr))
        check = (check * 131 + yes + rnd) % 1000000007
    print(f"10 rounds over 2000 arrays of 1000 values: checksum {check}")


main()
