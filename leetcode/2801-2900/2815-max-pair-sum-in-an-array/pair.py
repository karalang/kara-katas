# LeetCode #2815: Max Pair Sum in an Array -- the Python mirror of the ★
# arm: the largest number seen so far for each largest digit, and each
# number paired with the one held for its digit.


def largest_digit(x):
    top = 0
    while x > 0:
        top = max(top, x % 10)
        x //= 10
    return top


def max_sum(nums):
    best = [0] * 10
    answer = -1
    for x in nums:
        d = largest_digit(x)
        if best[d] > 0:
            answer = max(answer, best[d] + x)
        best[d] = max(best[d], x)
    return answer


seed = 2815


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(max_sum([51, 71, 17, 24, 42]))
    print(max_sum([1, 2, 3, 4]))
    print(max_sum([10000, 9999]))
    print(max_sum([9999, 9999]))
    print(max_sum(list(range(1, 101))))
    for count, extra, top, label in ((3000, 7, 100, "small"), (50, 99, 10000, "large")):
        none = 0
        check = 0
        for _ in range(count):
            n = next_random() % extra + 2
            nums = [next_random() % top + 1 for _ in range(n)]
            a = max_sum(nums)
            none += 1 if a == -1 else 0
            check = (check * 31 + a + 2) % 1000000007
        print(f"{count} {label} arrays: {none} without a pair, checksum {check}")


main()
