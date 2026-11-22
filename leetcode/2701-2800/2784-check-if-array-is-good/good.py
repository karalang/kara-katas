# LeetCode #2784: Check if Array is Good -- the ★ arm in Python
# (good.kara): every number from 1 to n counted, each of 1 to n - 1 once
# and n twice.


def is_good(nums):
    n = len(nums) - 1
    if n < 1:
        return False
    counts = [0] * (n + 1)
    for v in nums:
        if v < 1 or v > n:
            return False
        counts[v] += 1
    return all(counts[v] == 1 for v in range(1, n)) and counts[n] == 2


seed = 2784


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shuffled_base(n):
    nums = list(range(1, n + 1)) + [n]
    for i in range(n, 0, -1):
        j = next_random() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


def show(b):
    return "true" if b else "false"


def main():
    print(show(is_good([2, 1, 3])))
    print(show(is_good([1, 3, 3, 2])))
    print(show(is_good([1, 1])))
    print(show(is_good([3, 4, 4, 1, 2, 1])))
    print(show(is_good([1])))
    long = shuffled_base(99)
    print(show(is_good(long)))
    long[99] = 200
    print(show(is_good(long)))
    good = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        nums = shuffled_base(n)
        if next_random() % 3 != 0:
            at = next_random() % (n + 1)
            nums[at] = next_random() % 13 + 1
        g = is_good(nums)
        if g:
            good += 1
        check = (check * 31 + (2 if g else 1)) % 1000000007
    print(f"3000 small cases: {good} good, checksum {check}")


main()
