# LeetCode #1011 bench: the ★ arm (binary search on the capacity) over 20
# rows of 50,000 packages, drawn once; each of 20 rounds ships every row,
# each call with its own number of days, and folds each capacity into a
# checksum.


def ship_within_days(weights, days):
    lo = 0
    hi = 0
    for w in weights:
        lo = max(lo, w)
        hi += w
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if days_needed(weights, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo


def days_needed(weights, capacity):
    used = 1
    load = 0
    for w in weights:
        if load + w > capacity:
            used += 1
            load = 0
        load += w
    return used


seed = 1011


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 20, 20
    rows = [[1 + next_random() % 500 for _ in range(50000)] for _ in range(count)]
    check = 0
    for r in range(rounds):
        for k in range(count):
            days = 1 + ((r * count + k) * 7919) % 50000
            check = (check * 31 + ship_within_days(rows[k], days)) % 1000000007
    print(f"{rounds} rounds over {count} rows of 50000 packages: checksum {check}")


main()
