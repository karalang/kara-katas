# LeetCode #992: Subarrays with K Different Integers -- mirror of the ★
# arm (subarrays_with_k_distinct.kara), at most k less at most k - 1.


def at_most(nums, k):
    count = [0] * (len(nums) + 1)
    distinct = 0
    left = 0
    total = 0
    for right in range(len(nums)):
        if count[nums[right]] == 0:
            distinct += 1
        count[nums[right]] += 1
        while distinct > k:
            count[nums[left]] -= 1
            if count[nums[left]] == 0:
                distinct -= 1
            left += 1
        total += right - left + 1
    return total


def subarrays_with_k_distinct(nums, k):
    return at_most(nums, k) - at_most(nums, k - 1)


seed = 992


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shown(nums):
    if len(nums) > 12:
        return f"{len(nums)} numbers"
    return "[" + ", ".join(map(str, nums)) + "]"


def main():
    n = 20000
    cases = [
        ([1, 2, 1, 2, 3], 2),
        ([1, 2, 1, 3, 4], 3),
        ([1], 1),
        ([1, 1, 1, 1], 1),
        ([1, 2, 3, 4], 4),
        ([1, 1, 2], 3),
        ([1, 2, 1, 2, 1], 2),
        ([2, 1, 1, 1, 2], 1),
        ([1, 2, 3, 1, 2, 3], 3),
        ([3, 3, 1, 3, 2, 3, 1], 2),
    ]
    for nums, k in cases:
        print(f"nums = {shown(nums)}, k = {k} -> {subarrays_with_k_distinct(nums, k)}")
    distinct = [i + 1 for i in range(n)]
    print(f"20000 different numbers, k = 1 -> {subarrays_with_k_distinct(distinct, 1)}")
    print(f"20000 different numbers, k = 20000 -> {subarrays_with_k_distinct(distinct, 20000)}")
    print(f"20000 ones, k = 1 -> {subarrays_with_k_distinct([1] * n, 1)}")
    cycle = [i % 100 + 1 for i in range(n)]
    print(f"1 to 100 repeated to 20000 numbers, k = 50 -> {subarrays_with_k_distinct(cycle, 50)}")
    for count, most, values in [(300, 8, 3), (3000, 60, 10), (300, 1000, 30), (3, 20000, 200)]:
        total = 0
        found = 0
        check = 0
        for _ in range(count):
            m = most if count == 3 else 1 + next_random() % most
            nums = [1 + next_random() % min(values, m) for _ in range(m)]
            k = 1 + next_random() % min(values, m)
            got = subarrays_with_k_distinct(nums, k)
            total += m
            found += got
            check = (check * 31 + got + 1) % 1000000007
        print(f"{count} random arrays of up to {most} numbers below {values + 1}: {total} numbers, {found} subarrays, checksum {check}")


main()
