# LeetCode #1498: Number of Subsequences That Satisfy the Given Sum
# Condition -- the bench in Python, mirroring num_subseq.kara: the values
# sorted, then two pointers.

MOD = 1000000007


def num_subseq(nums, target):
    s = sorted(nums)
    n = len(s)
    pow2 = [1] * n
    for i in range(1, n):
        pow2[i] = pow2[i - 1] * 2 % MOD
    count = 0
    lo, hi = 0, n - 1
    while lo <= hi:
        if s[lo] + s[hi] <= target:
            count = (count + pow2[hi - lo]) % MOD
            lo += 1
        else:
            hi -= 1
    return count


def main():
    seed = 1498
    nums = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        nums.append(1 + seed // 65536 * 31 % 1000000)
    check = 0
    for call in range(200):
        at = (check + call * 7919) % 100000
        nums[at] = 1 + (check + call) % 1000000
        target = 1 + (check * 13 + call) % 1000000
        check = (check * 31 + num_subseq(nums, target)) % 1000000007
    print(f"200 calls over 100000 values: checksum {check}")


main()
