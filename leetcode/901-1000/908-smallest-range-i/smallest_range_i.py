# LeetCode #908: Smallest Range I -- Python mirror of the largest and
# smallest values in smallest_range_i.kara, with the same test harness.


def smallest_range_i(nums, k):
    lo = nums[0]
    hi = nums[0]
    for i in range(1, len(nums)):
        lo = min(lo, nums[i])
        hi = max(hi, nums[i])
    return max(hi - lo - 2 * k, 0)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums, k):
    listed = ",".join(str(x) for x in nums)
    print(f"nums = [{listed}], k = {k} -> {smallest_range_i(nums, k)}")


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
    seed = 908
    total = 0
    check = 0
    for c in range(300):
        length = 1 + next_random() % 2000
        top = 10 if c % 3 == 0 else 1000 if c % 3 == 1 else 10001
        nums = [next_random() % top for _ in range(length)]
        k = next_random() % (top // 2 + 1)
        got = smallest_range_i(nums, k)
        total += got
        check = (check * 1000003 + got) % 1000000007
    print(f"300 cases: scores summing to {total}, checksum {check}")
    big = [next_random() % 10001 for _ in range(10000)]
    print(f"10000 numbers, k = 0 -> {smallest_range_i(big, 0)}")
    print(f"10000 numbers, k = 2500 -> {smallest_range_i(big, 2500)}")


main()
