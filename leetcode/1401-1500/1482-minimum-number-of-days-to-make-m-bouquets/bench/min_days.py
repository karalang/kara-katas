# LeetCode #1482: Minimum Number of Days to Make m Bouquets -- bench, the
# Python twin of min_days.kara.


def bouquets(bloom_day, k, day):
    made = 0
    run = 0
    for d in bloom_day:
        if d <= day:
            run += 1
            if run == k:
                made += 1
                run = 0
        else:
            run = 0
    return made


def min_days(bloom_day, m, k):
    if m * k > len(bloom_day):
        return -1
    lo = min(bloom_day)
    hi = max(bloom_day)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if bouquets(bloom_day, k, mid) >= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


seed = 1482


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    bloom = []
    for _ in range(100000):
        hi = next_random()
        lo = next_random()
        bloom.append(1 + (hi * 32768 + lo) % 1000000000)
    check = 0
    for p in range(150):
        bloom[check % 100000] = 1 + (check * 7) % 1000000000
        k = 1 + check % 10
        m = 1 + (check // 10) % (100000 // k + 100)
        check = (check * 31 + min_days(bloom, m, k) + 1 + p) % 1000000007
    print(f"150 passes over 100000 flowers: checksum {check}")


main()
