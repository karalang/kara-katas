# LeetCode #915: Partition Array into Disjoint Intervals -- Python mirror
# of the largest on the left against the smallest on the right in
# partition_disjoint.kara, with the same test harness.


def partition_disjoint(nums):
    n = len(nums)
    least_after = [0] * n
    least_after[n - 1] = nums[n - 1]
    i = n - 1
    while i > 0:
        i -= 1
        least_after[i] = min(nums[i], least_after[i + 1])
    most = nums[0]
    for k in range(1, n):
        if most <= least_after[k]:
            return k
        most = max(most, nums[k])
    return n


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    s = ",".join(str(v) for v in nums)
    print(f"nums = [{s}]: {partition_disjoint(nums)}")


def random_nums(left, right, cut, top):
    nums = []
    for _ in range(left):
        nums.append(next_random() % (cut + 1))
    for _ in range(right):
        nums.append(cut + next_random() % (top - cut + 1))
    return nums


def big():
    high = next_random()
    return (high * 32768 + next_random()) % 1000001


def main():
    global seed
    show([5, 0, 3, 8, 6])
    show([1, 1, 1, 0, 6, 12])
    show([1, 1])
    show([0, 1000000])
    show([2, 1, 3])
    show([3, 1, 2, 4, 3, 5])
    show([1, 2, 3, 4, 5])
    show([4, 3, 2, 1, 5])
    show([7, 7, 7, 7])
    seed = 915
    check = 0
    total = 0
    for c in range(500):
        n = 2 + next_random() % 999
        left = 1 + next_random() % (n - 1)
        top = 5 if c % 3 == 0 else 1000 if c % 3 == 1 else 1000000
        cut = next_random() % (top + 1)
        k = partition_disjoint(random_nums(left, n - left, cut, top))
        total += k
        check = (check * 1000003 + k) % 1000000007
    print(f"500 arrays: lengths summing to {total}, checksum {check}")
    rising = [i * 10 for i in range(100000)]
    print(f"100000 rising: {partition_disjoint(rising)}")
    late = []
    for i in range(100000):
        late.append(0 if i == 99998 else 1000000 if i == 99999 else 1 + big() % 999999)
    print(f"100000 with the smallest second to last: {partition_disjoint(late)}")
    half = random_nums(50000, 50000, 500000, 1000000)
    print(f"100000 in two halves: {partition_disjoint(half)}")


main()
