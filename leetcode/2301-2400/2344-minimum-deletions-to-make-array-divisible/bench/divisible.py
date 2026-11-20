# LeetCode #2344: Minimum Deletions to Make Array Divisible -- the bench,
# the ★ arm in Python: the gcd of numsDivide, then nums sorted and scanned
# for the first value that divides it.


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def min_operations(nums, nums_divide):
    g = 0
    for x in nums_divide:
        g = gcd(g, x)
    s = sorted(nums)
    for i in range(len(s)):
        if g % s[i] == 0:
            return i
    return -1


def scrambled(index):
    return index * 2654435761 % 2147483647


def main():
    cases = []
    for a in range(10):
        nums = [scrambled(a * 100000 + i) % 1000000 + 1 for i in range(100000)]
        base = nums[a * 7919 % 100000]
        nums_divide = [base * (scrambled(a * 10000 + i + 7) % 1000 + 1) for i in range(10000)]
        cases.append((nums, nums_divide))
    check = 0
    for p in range(20):
        for nums, nums_divide in cases:
            check = (check * 31 + min_operations(nums, nums_divide) + p) % 1000000007
    print(f"20 passes over 10 cases of 10^5 values against 10^4: checksum {check}")


main()
