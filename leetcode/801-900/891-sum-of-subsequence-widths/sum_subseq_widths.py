# LeetCode #891: Sum of Subsequence Widths -- Python mirror of the sorted
# solution in sum_subseq_widths.kara, with the same test harness.
#
# A subsequence's width depends only on which values it holds, so sort
# them. The value at sorted position i is the largest of the 2^i
# subsequences made of it and any of the i values before it, and the
# smallest of the 2^(n-1-i) made of it and any after it; it adds itself
# to the width of the first and takes itself away from the second.
# O(n log n).

MODULUS = 1000000007


def sum_subseq_widths(nums):
    a = sorted(nums)
    n = len(a)
    pow2 = [1] * n
    for i in range(1, n):
        pow2[i] = pow2[i - 1] * 2 % MODULUS
    total = 0
    for i in range(n):
        total = (total + a[i] * (pow2[i] - pow2[n - 1 - i])) % MODULUS
    return total


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"nums = [{', '.join(map(str, nums))}] -> {sum_subseq_widths(nums)}")


def main():
    global seed
    show([2, 1, 3])
    show([2])
    show([7, 7, 7])
    show([1, 2])
    show([5, 1, 4, 2, 3, 3])
    # 1 to 40, where the widths overflow the modulus many times
    show(list(range(1, 41)))
    # random cases: up to 200 numbers, from 1 to 100000 or, a third of
    # the time, from 1 to 10 so that values repeat
    seed = 891
    numbers = 0
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 200
        top = 10 if next_random() % 3 == 0 else 100000
        nums = [1 + next_random() % top for _ in range(n)]
        got = sum_subseq_widths(nums)
        numbers += n
        total = (total + got) % MODULUS
        check = (check * 131 + got) % MODULUS
    print(f"2000 cases of up to 200 numbers ({numbers} in all): widths sum to {total}, checksum {check}")


main()
