# LeetCode #2741: Special Permutations -- Python mirror of special.kara
# (the ★ arm): ways[mask][last] carried forward to every partner of
# `last` outside the mask.

MOD = 1000000007


def special_perm(nums):
    n = len(nums)
    full = (1 << n) - 1
    ways = [[0] * n for _ in range(1 << n)]
    for i in range(n):
        ways[1 << i][i] = 1
    for mask in range(1, full):
        for last in range(n):
            w = ways[mask][last]
            if w == 0:
                continue
            for nxt in range(n):
                if (mask >> nxt) & 1 == 0 and (nums[nxt] % nums[last] == 0 or nums[last] % nums[nxt] == 0):
                    to = mask | (1 << nxt)
                    ways[to][nxt] = (ways[to][nxt] + w) % MOD
    total = 0
    for last in range(n):
        total = (total + ways[full][last]) % MOD
    return total


seed = 2741


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_smooth(n):
    nums = []
    while len(nums) < n:
        a = next_random() % 6
        b = next_random() % 4
        x = (1 << a) * [1, 3, 9, 27][b]
        if x not in nums:
            nums.append(x)
    return nums


def random_numbers(n, most):
    nums = []
    while len(nums) < n:
        x = next_random() % most + 1
        if x not in nums:
            nums.append(x)
    return nums


def main():
    print(special_perm([2, 3, 6]))
    print(special_perm([1, 4, 3]))
    print(special_perm([1, 2]))
    print(special_perm([2, 3]))
    print(special_perm([1 << k for k in range(14)]))
    total = check = 0
    for c in range(2010):
        if c < 2000:
            n = next_random() % 7 + 2
            nums = random_smooth(n) if c % 2 == 0 else random_numbers(n, 30)
        else:
            nums = random_smooth(14)
        count = special_perm(nums)
        total += count
        check = (check * 31 + count) % 1000000007
        if c == 1999:
            print(f"2000 small arrays: counts sum to {total}, checksum {check}")
            total = check = 0
    print(f"10 arrays of 14 numbers: counts sum to {total}, checksum {check}")


main()
