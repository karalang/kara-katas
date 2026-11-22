# LeetCode #2780: Minimum Index of a Valid Split -- the ★ arm in Python
# (split.kara): the dominant number by Boyer-Moore's vote, counted, then
# the first split where it is more than half of each side.


def minimum_index(nums):
    n = len(nums)
    x = 0
    votes = 0
    for v in nums:
        if votes == 0:
            x = v
        votes += 1 if v == x else -1
    total = sum(1 for v in nums if v == x)
    left = 0
    for i in range(n - 1):
        if nums[i] == x:
            left += 1
        if 2 * left > i + 1 and 2 * (total - left) > n - i - 1:
            return i
    return -1


seed = 2780


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


# n numbers with a dominant one: more than half of them x, the rest drawn
# from `others` values, shuffled
def dominated(n, others, top):
    x = wide() % top + 1
    many = n // 2 + 1 + wide() % (n - n // 2)
    nums = [x] * many
    while len(nums) < n:
        v = wide() % others + 1
        if v != x:
            nums.append(v)
    for i in range(n - 1, 0, -1):
        j = wide() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


def main():
    print(minimum_index([1, 2, 2, 2]))
    print(minimum_index([2, 1, 3, 1, 1, 1, 7, 1, 2, 1]))
    print(minimum_index([3, 3, 3, 3, 7, 2, 2]))
    print(minimum_index([5]))
    n = 100000
    print(minimum_index([1000000000] * n))
    print(minimum_index([i + 2 if i < 49999 else 1 for i in range(n)]))
    found = total = check = 0
    for _ in range(3000):
        m = next_random() % 12 + 1
        a = minimum_index(dominated(m, 4, 4))
        if a >= 0:
            found += 1
            total += a
        check = (check * 31 + a + 1) % 1000000007
    print(f"3000 small arrays: {found} split, indices sum to {total}, checksum {check}")
    found = total = check = 0
    for _ in range(20):
        a = minimum_index(dominated(n, 1000000000, 1000000000))
        if a >= 0:
            found += 1
            total += a
        check = (check * 31 + a + 1) % 1000000007
    print(f"20 arrays of 10^5: {found} split, indices sum to {total}, checksum {check}")


main()
