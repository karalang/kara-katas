# Benchmark for #454: mirror of four_sum.kara (the ★ arm, pair sums of
# the first two arrays counted in a map) on the same workload.


def four_sum_count(nums1, nums2, nums3, nums4):
    sums = {}
    for a in nums1:
        for b in nums2:
            sums[a + b] = sums.get(a + b, 0) + 1
    count = 0
    for c in nums3:
        for d in nums4:
            count += sums.get(-(c + d), 0)
    return count


# ---- benchmark --------------------------------------------------------

seed = 454


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value():
    hi = next_random()
    lo = next_random()
    return (hi * 65536 + lo) % 100001 - 50000


def main():
    n = 1000
    rounds = 10
    arrays = []
    for _ in range(4):
        arrays.append([random_value() for _ in range(n)])
    total = 0
    checksum = 0
    for _ in range(rounds):
        for a in range(4):
            at = next_random() % n
            arrays[a][at] = random_value()
        tuples = four_sum_count(arrays[0], arrays[1], arrays[2], arrays[3])
        total += tuples
        checksum = (checksum * 31 + tuples) % 1000000007
    print(f"{rounds} rounds on 4 arrays of {n}: {total} tuples, checksum {checksum}")


main()
