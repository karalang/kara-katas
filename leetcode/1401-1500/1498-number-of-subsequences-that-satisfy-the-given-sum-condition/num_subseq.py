# LeetCode #1498: Number of Subsequences That Satisfy the Given Sum
# Condition -- the Python mirror of num_subseq.kara: the values sorted, then
# two pointers.

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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    print(f"{num_subseq([3, 5, 6, 7], 9)} {num_subseq([3, 3, 6, 8], 10)} {num_subseq([2, 3, 3, 4, 6, 7], 12)}")
    print(f"{num_subseq([1], 2)} {num_subseq([2], 3)} {num_subseq([9, 8, 7], 6)} {num_subseq([4, 4, 4, 4], 8)} {num_subseq([5, 7, 9], 10)} {num_subseq([1, 9], 10)}")
    ones = [1] * 100000
    seed = 1498
    big = [1 + next_random() * 31 % 1000000 for _ in range(100000)]
    print(f"100000 values: {num_subseq(ones, 2)} {num_subseq(big, 1000000)} {num_subseq(big, 500000)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        nums = [1 + next_random() % 50 for _ in range(n)]
        target = 1 + next_random() % 100
        check = (check * 31 + num_subseq(nums, target)) % 1000000007
    print(f"3000 random arrays: checksum {check}")


main()
