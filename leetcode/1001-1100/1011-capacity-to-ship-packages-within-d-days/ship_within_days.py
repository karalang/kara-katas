# LeetCode #1011: Capacity To Ship Packages Within D Days -- binary search
# on the capacity. Mirrors ship_within_days.kara line for line.


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


def show(nums):
    return "[" + ",".join(str(x) for x in nums) + "]"


def main():
    examples = [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5),
        ([3, 2, 2, 4, 1, 4], 3),
        ([1, 2, 3, 1, 1], 4),
        ([500], 1),
        ([1, 1, 1, 1], 4),
        ([1, 1, 1, 1], 1),
        ([10, 50, 100, 100, 50, 10], 2),
        ([7, 2, 5, 10, 8], 2),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10),
    ]
    for weights, days in examples:
        print(f"weights = {show(weights)}, days = {days} -> {ship_within_days(weights, days)}")
    heavy = [500] * 50000
    cycle = [1 + i % 500 for i in range(50000)]
    large = [
        ("50000 packages of 500, 1 day", heavy, 1),
        ("50000 packages of 500, 50000 days", heavy, 50000),
        ("50000 packages of 500, 7 days", heavy, 7),
        ("50000 packages cycling 1..500, 100 days", cycle, 100),
        ("50000 packages cycling 1..500, 49999 days", cycle, 49999),
    ]
    for name, weights, days in large:
        print(f"{name} -> {ship_within_days(weights, days)}")
    for count, most in [(2000, 10), (200, 1000), (5, 50000)]:
        packages = 0
        total = 0
        check = 0
        for _ in range(count):
            size = 1 + next_random() % most
            top = 1 + next_random() % 500
            weights = [1 + next_random() % top for _ in range(size)]
            days = 1 + next_random() % size
            capacity = ship_within_days(weights, days)
            packages += size
            total += capacity
            check = (check * 31 + capacity) % 1000000007
        print(f"{count} random shipments of {packages} packages: capacities sum to {total}, checksum {check}")


main()
