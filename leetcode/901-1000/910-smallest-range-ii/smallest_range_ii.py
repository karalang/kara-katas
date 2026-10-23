# LeetCode #910: Smallest Range II -- Python mirror of the sorted values
# split in two in smallest_range_ii.kara, with the same test harness.


def smallest_range_ii(nums, k):
    a = sorted(nums)
    n = len(a)
    best = a[n - 1] - a[0]
    for i in range(n - 1):
        hi = max(a[i] + k, a[n - 1] - k)
        lo = min(a[0] + k, a[i + 1] - k)
        best = min(best, hi - lo)
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums, k):
    listed = ",".join(str(x) for x in nums)
    print(f"nums = [{listed}], k = {k} -> {smallest_range_ii(nums, k)}")


def main():
    global seed
    show([1], 0)
    show([0, 10], 2)
    show([1, 3, 6], 3)
    show([7, 7, 7], 0)
    show([0, 10000], 0)
    show([0, 10000], 10000)
    show([2, 9, 4, 13, 5], 2)
    show([2, 9, 4, 13, 5], 5)
    seed = 910
    total = 0
    check = 0
    for c in range(300):
        length = 1 + next_random() % 2000
        top = 10 if c % 3 == 0 else 1000 if c % 3 == 1 else 10001
        nums = [next_random() % top for _ in range(length)]
        k = next_random() % (top // 2 + 1)
        got = smallest_range_ii(nums, k)
        total += got
        check = (check * 1000003 + got) % 1000000007
    print(f"300 cases: scores summing to {total}, checksum {check}")
    big = [next_random() % 10001 for _ in range(10000)]
    print(f"10000 numbers, k = 0 -> {smallest_range_ii(big, 0)}")
    print(f"10000 numbers, k = 2500 -> {smallest_range_ii(big, 2500)}")


main()
