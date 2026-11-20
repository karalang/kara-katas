# LeetCode #2342: Max Sum of a Pair With Equal Sum of Digits -- the Python
# mirror of the ★ arm: the largest value seen for each digit sum, and each
# value paired with the largest before it of its own digit sum.


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


SEED = [2342]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    print(maximum_sum([18, 43, 36, 13, 7]))
    print(maximum_sum([10, 12, 19, 14]))
    print(maximum_sum([1]))
    print(maximum_sum([999999999, 999999999]))
    print(maximum_sum([1000000000, 1, 10, 100]))
    big = [(i * 982451653 + 13) % 1000000000 + 1 for i in range(2000)]
    print(maximum_sum(big))
    check = 0
    total = 0
    found = 0
    for _ in range(2000):
        n = 1 + next_random() % 30
        top = [10, 100, 10000, 1000000000][next_random() % 4]
        nums = [1 + (next_random() * 32768 + next_random()) % top for _ in range(n)]
        answer = maximum_sum(nums)
        check = (check * 31 + answer + 1) % 1000000007
        total += answer
        if answer >= 0:
            found += 1
    print(f"2000 cases: checksum {check}, sum {total}, with a pair {found}")


main()
