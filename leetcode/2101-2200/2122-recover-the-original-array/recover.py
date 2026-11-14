# LeetCode #2122: Recover the Original Array -- the mirror of
# recover.kara: each positive even distance from the smallest number
# tried as 2k, smallest first, and the sorted numbers paired by two
# pointers.


def recover_array(nums):
    s = sorted(nums)
    m = len(s)
    for i in range(1, m):
        gap = s[i] - s[0]
        if gap == 0 or gap % 2 != 0 or (i > 1 and gap == s[i - 1] - s[0]):
            continue
        k = gap // 2
        used = [False] * m
        original = []
        high = 0
        for low in range(m):
            if used[low]:
                continue
            while high < m and (used[high] or high <= low or s[high] < s[low] + 2 * k):
                high += 1
            if high == m or s[high] != s[low] + 2 * k:
                break
            used[high] = True
            original.append(s[low] + k)
        if len(original) * 2 == m:
            return original
    return []


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    examples = [
        [2, 10, 6, 4, 8, 12],
        [1, 1, 3, 3],
        [5, 435],
        [7, 9],
        [4, 4, 4, 10, 10, 10],
        [1, 3, 4, 6, 9, 11],
        [999999998, 1000000000, 1, 3],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {show(sorted(recover_array(nums)))}")
    seed = [2122]
    sizes = 0
    check = 0
    for rnd in range(2000):
        n = next_random(seed) % 12 + 1
        top = [1, 10, 1000][rnd % 3]
        k = next_random(seed) % 20 + 1
        nums = []
        for _ in range(n):
            x = next_random(seed) % top + 1 + k
            nums.append(x - k)
            nums.append(x + k)
        for i in range(len(nums) - 1, 0, -1):
            j = next_random(seed) % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        got = sorted(recover_array(nums))
        sizes += len(got)
        for v in got:
            check = (check * 31 + v) % 1000000007
    print(f"2000 arrays: {sizes} values recovered, checksum {check}")
    big = []
    for _ in range(1000):
        x = (next_random(seed) * 32768 + next_random(seed)) % 1000000 + 778
        big.append(x - 777)
        big.append(x + 777)
    got = recover_array(big)
    print(f"2000 values: {len(got)} recovered, sum {sum(got)}")


main()
