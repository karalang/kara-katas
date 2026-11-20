# LeetCode #2401: Longest Nice Subarray -- the Python mirror of the ★
# arm: a sliding window keeping the OR of its values.

seed = 2401


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def longest_nice_subarray(nums):
    used = 0
    left = 0
    best = 0
    for right in range(len(nums)):
        while used & nums[right] != 0:
            used ^= nums[left]
            left += 1
        used |= nums[right]
        best = max(best, right - left + 1)
    return best


def main():
    print(longest_nice_subarray([1, 3, 8, 48, 10]))
    print(longest_nice_subarray([3, 1, 5, 11, 13]))
    print(longest_nice_subarray([1000000000]))
    powers = [1 << b for b in range(30)]
    print(longest_nice_subarray(powers))
    print(longest_nice_subarray(powers + powers))
    big = [1 + wide() % 1000000000 for _ in range(100000)]
    print(longest_nice_subarray(big))
    bits = [1 << (next_random() % 30) for _ in range(100000)]
    print(longest_nice_subarray(bits))
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        nums = []
        for _ in range(n):
            x = 0
            for _ in range(1 + next_random() % 3):
                x |= 1 << (next_random() % 12)
            nums.append(x)
        a = longest_nice_subarray(nums)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
