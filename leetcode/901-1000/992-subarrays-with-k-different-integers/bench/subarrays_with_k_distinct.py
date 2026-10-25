# LeetCode #992: Subarrays with K Different Integers -- bench, the ★ arm
# (at most k, less at most k - 1), the same algorithm and workload as
# subarrays_with_k_distinct.kara.


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


def main():
    rounds = 100
    arrays = [[1 + next_random() % 100 for _ in range(20000)] for _ in range(20)]
    found = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            k = 1 + (r * 7 + i) % 60
            got = subarrays_with_k_distinct(arrays[(r + i) % 20], k)
            found += got
            check = (check * 31 + got + 1) % 1000000007
    print(f"{rounds} rounds over 20 arrays of 20000 numbers: {found} subarrays, checksum {check}")


main()
