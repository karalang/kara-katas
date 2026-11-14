# LeetCode #2122: Recover the Original Array -- the benchmark, the same
# algorithm as recover.kara: each positive even distance from the
# smallest number tried as 2k, smallest first, the sorted numbers paired
# by two pointers.


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


def main():
    seed = [2122]
    arrays = []
    for g in range(40):
        top = [1000, 10000, 100000][g % 3]
        k = next_random(seed) % 500 + 1
        nums = []
        for _ in range(1000):
            x = (next_random(seed) * 32768 + next_random(seed)) % top + 1 + k
            nums.append(x - k)
            nums.append(x + k)
        for i in range(len(nums) - 1, 0, -1):
            j = next_random(seed) % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        arrays.append(nums)
    sizes = 0
    check = 0
    for _ in range(200):
        for g in range(40):
            arr = arrays[g]
            for i in range(len(arr)):
                arr[i] += 1
            original = recover_array(arr)
            sizes += len(original)
            for v in original:
                check = (check * 31 + v) % 1000000007
    print(f"8000 solves: {sizes} values recovered, checksum {check}")


main()
