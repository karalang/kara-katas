# LeetCode #454: 4Sum II -- mirror of four_sum.kara (pair sums of the
# first two arrays in a map, looked up from the last two), with the same
# harness.


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


# ---- test harness ---------------------------------------------------------


def listed(nums):
    return ",".join(str(x) for x in nums)


def show(nums1, nums2, nums3, nums4):
    count = four_sum_count(nums1, nums2, nums3, nums4)
    print(f"[{listed(nums1)}] [{listed(nums2)}] [{listed(nums3)}] [{listed(nums4)}]: {count} tuples")


seed = 454


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, spread):
    nums = []
    for _ in range(n):
        r = next_random() * 65536
        r += next_random()
        nums.append(r % spread - spread // 2)
    return nums


def main():
    show([1, 2], [-2, -1], [-1, 2], [0, 2])
    show([0], [0], [0], [0])
    show([1], [1], [1], [1])
    show([0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0])
    show([268435456, -268435456], [268435456, -268435456], [-268435456], [-268435456, 268435456])
    show([1, -1, 2], [-2, 1, 0], [3, -3, 0], [0, 1, -1])
    # 300 random cases of 1 to 40 numbers in each array, spread over 3,
    # 11, 101 or every value from -2^28 to 2^28.
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        n = 1 + next_random() % 40
        spread = [3, 11, 101, 536870913][next_random() % 4]
        nums1 = random_nums(n, spread)
        nums2 = random_nums(n, spread)
        nums3 = random_nums(n, spread)
        nums4 = random_nums(n, spread)
        tuples = four_sum_count(nums1, nums2, nums3, nums4)
        total += tuples
        checksum = (checksum * 31 + tuples) % 1000000007
    print(f"{count} random cases: {total} tuples, checksum {checksum}")


main()
