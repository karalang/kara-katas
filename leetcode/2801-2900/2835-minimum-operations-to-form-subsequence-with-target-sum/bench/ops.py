# LeetCode #2835: Minimum Operations to Form Subsequence With Target Sum
# -- the bench, mirrored from ops.kara: counts by bit, low to high.


def min_operations(nums, target):
    if sum(nums) < target:
        return -1
    count = [0] * 32
    for x in nums:
        count[(x & -x).bit_length() - 1] += 1
    ops = 0
    for i in range(31):
        if (target >> i) & 1:
            if count[i] > 0:
                count[i] -= 1
            else:
                j = i + 1
                while count[j] == 0:
                    j += 1
                ops += j - i
                count[j] -= 1
                for k in range(i, j):
                    count[k] += 1
        count[i + 1] += count[i] // 2
    return ops


seed = 2835


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 2000, 200, 1000
    cases = []
    for _ in range(count):
        nums = [1 << (next_random() % 15 + 16) for _ in range(n)]
        hi = next_random()
        target = (hi * 32768 + next_random()) % 2147483647 + 1
        cases.append((nums, target))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, target in cases:
            ops = min_operations(nums, target)
            total += ops
            check = (check * 31 + ops + 1 + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: operations total {total}, checksum {check}")


main()
