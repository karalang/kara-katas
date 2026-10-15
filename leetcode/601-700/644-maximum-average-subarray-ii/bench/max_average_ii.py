# Benchmark for #644: mirror of max_average_ii.kara (the ★ arm: binary
# search on the average) on the same workload.


def reaches(prefix, k, m):
    lowest = 0
    for end in range(k, len(prefix)):
        c = end - k
        if float(prefix[c] - prefix[lowest]) < m * float(c - lowest):
            lowest = c
        if float(prefix[end] - prefix[lowest]) >= m * float(end - lowest):
            return (lowest, end)
    return (-1, -1)


def find_max_average(nums, k):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    lo = float(nums[0])
    hi = float(nums[0])
    for x in nums:
        lo = min(lo, float(x))
        hi = max(hi, float(x))
    best = (0, len(nums))
    for _ in range(100):
        mid = (lo + hi) / 2.0
        start, end = reaches(prefix, k, mid)
        if start == -1:
            hi = mid
        else:
            lo = mid
            best = (start, end)
    start, end = best
    return float(prefix[end] - prefix[start]) / float(end - start)


def main():
    seed = 644

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    for _ in range(20):
        arrays.append([next_random() % 20001 - 10000 for _ in range(100000)])
    rounds = 40
    total = 0.0
    for r in range(rounds):
        k = 1 + (r * 7919) % 100000
        total += find_max_average(arrays[r % 20], k)
    print(f"{rounds} rounds over 20 arrays of 100000 values: answers adding to {total:.5f}")


main()
