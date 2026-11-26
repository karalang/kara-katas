# LeetCode #1482: Minimum Number of Days to Make m Bouquets -- Python
# mirror of min_days.kara: a binary search over the days, each day's
# bouquets counted by a walk along the garden


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
    lo, hi = min(bloom_day), max(bloom_day)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if bouquets(bloom_day, k, mid) >= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---- test harness ---------------------------------------------------------

seed = 1482


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def draw(n, top):
    return [1 + wide_random() % top for _ in range(n)]


def main():
    l1 = min_days([1, 10, 3, 10, 2], 3, 1)
    l2 = min_days([1, 10, 3, 10, 2], 3, 2)
    l3 = min_days([7, 7, 7, 7, 12, 7, 7], 2, 3)
    print(f"{l1} {l2} {l3}")
    e = [
        min_days([5], 1, 1),
        min_days([3, 1, 4, 1, 5], 1, 5),
        min_days([3, 1, 4, 1, 5], 3, 2),
        min_days([1000000000, 1000000000], 1, 2),
        min_days([1, 1, 9, 1, 1, 2, 2], 3, 2),
        min_days([1, 9, 1], 1, 3),
    ]
    print(" ".join(map(str, e)))
    garden = draw(100000, 1000000000)
    asks = [(1, 1), (100, 50), (900, 100), (50000, 2), (100000, 1)]
    most = [str(min_days(garden, m, k)) for m, k in asks]
    print(f"100000 flowers: {' '.join(most)}")
    check = 0
    none = 0
    for _ in range(3000):
        n = 1 + next_random() % 60
        top = 1 + wide_random() % 1000000000
        g = draw(n, top)
        m = 1 + next_random() % 10
        k = 1 + next_random() % 6
        got = min_days(g, m, k)
        if got == -1:
            none += 1
        check = (check * 31 + got + 1) % 1000000007
    print(f"3000 random gardens: {none} with no way, checksum {check}")


main()
