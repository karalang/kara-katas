# LeetCode #2741: Special Permutations -- the bench (special.kara in
# Python): ways[mask][last] carried forward to every partner of `last`.

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


def main():
    count, rounds = 30, 5
    seed = 2741
    arrays = []
    for _ in range(count):
        nums = []
        while len(nums) < 14:
            seed = (seed * 1103515245 + 12345) % 2147483648
            a = seed // 65536 % 6
            seed = (seed * 1103515245 + 12345) % 2147483648
            b = seed // 65536 % 4
            x = (1 << a) * [1, 3, 9, 27][b]
            if x not in nums:
                nums.append(x)
        arrays.append(nums)
    total = check = 0
    for r in range(rounds):
        for nums in arrays:
            k = special_perm(nums)
            total += k
            check = (check * 31 + k + r) % 1000000007
    print(f"{count} arrays of 14 numbers, {rounds} rounds: counts sum to {total}, checksum {check}")


main()
