# LeetCode #2870: Minimum Number of Operations to Make Array Empty --
# the bench, as empty.kara: 50 arrays of 10^5 values, each answered 10
# times by the sorted-runs arm.

def min_operations(nums):
    s = sorted(nums)
    ops = 0
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        f = j - i
        if f == 1:
            return -1
        ops += (f + 2) // 3
        i = j
    return ops


seed = 2870


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 50, 10, 100000
    arrays = []
    for _ in range(count):
        nums = []
        while len(nums) < n:
            v = wide() % 1000000 + 1
            copies = min(next_random() % 7 + 2, n - len(nums))
            nums.extend([v] * copies)
        for i in range(n - 1, 0, -1):
            j = wide() % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        arrays.append(nums)
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            ops = min_operations(nums)
            total += ops
            check = (check * 31 + ops + 1 + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: {total} operations, checksum {check}")


main()
