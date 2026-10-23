# LeetCode #891 bench: Python mirror of sum_subseq_widths.kara (the
# counting arm, a count of each value) on the same 400 arrays.

MODULUS = 1000000007


def sum_subseq_widths(nums):
    n = len(nums)
    largest = max(nums)
    count = [0] * (largest + 1)
    for x in nums:
        count[x] += 1
    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = pow2[i - 1] * 2 % MODULUS
    total = 0
    p = 0
    for v in range(largest + 1):
        c = count[v]
        if c > 0:
            block = pow2[c] - 1
            as_max = pow2[p] * block % MODULUS
            as_min = pow2[n - p - c] * block % MODULUS
            total = (total + v * (as_max - as_min)) % MODULUS
            p += c
    return total


def main():
    seed = 891
    total = 0
    check = 0
    for _ in range(400):
        nums = []
        for _ in range(100000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            nums.append(1 + seed // 65536 % 100000)
        got = sum_subseq_widths(nums)
        total = (total + got) % MODULUS
        check = (check * 131 + got) % MODULUS
    print(f"400 arrays of 100000 numbers: widths sum to {total}, checksum {check}")


main()
