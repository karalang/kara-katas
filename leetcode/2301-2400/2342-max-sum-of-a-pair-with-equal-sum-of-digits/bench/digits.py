# LeetCode #2342: Max Sum of a Pair With Equal Sum of Digits -- the bench,
# the ★ arm in Python: a table of 82 keeping the largest value seen for
# each digit sum, each value paired with the largest before it of its own
# sum.


def digit_sum(x):
    s = 0
    while x > 0:
        s += x % 10
        x //= 10
    return s


def maximum_sum(nums):
    best = [-1] * 82
    answer = -1
    for x in nums:
        s = digit_sum(x)
        if best[s] >= 0:
            answer = max(answer, best[s] + x)
        best[s] = max(best[s], x)
    return answer


def scrambled(index):
    return index * 2654435761 % 2147483647


def main():
    arrays = [[scrambled(a * 100000 + i) % 1000000000 + 1 for i in range(100000)] for a in range(10)]
    check = 0
    for p in range(20):
        for nums in arrays:
            check = (check * 31 + maximum_sum(nums) + p) % 1000000007
    print(f"20 passes over 10 arrays of 10^5 values: checksum {check}")


main()
