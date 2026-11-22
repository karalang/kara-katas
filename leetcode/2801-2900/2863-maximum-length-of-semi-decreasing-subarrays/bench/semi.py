# LeetCode #2863: Maximum Length of Semi-Decreasing Subarrays -- the
# bench: the ★ arm over 100 arrays of 10^5 values, LeetCode's most,
# every other one random over LeetCode's range and the rest rising with
# five values moved, all drawn first, then each answered 10 times.


def max_subarray_length(nums):
    n = len(nums)
    starts = []
    for i in range(n):
        if not starts or nums[i] > nums[starts[-1]]:
            starts.append(i)
    best = 0
    for j in range(n - 1, -1, -1):
        while starts and nums[starts[-1]] > nums[j]:
            best = max(best, j - starts[-1] + 1)
            starts.pop()
    return best


def main():
    count, rounds, n = 100, 10, 100000
    seed = 2863

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide():
        a = nr()
        return a * 32768 + nr()

    arrays = []
    for c in range(count):
        if c % 2 == 0:
            nums = [wide() % 2000000001 - 1000000000 for _ in range(n)]
        else:
            nums = [20000 * i - 1000000000 for i in range(n)]
            for _ in range(5):
                i = wide() % n
                nums[i] = wide() % 2000000001 - 1000000000
        arrays.append(nums)
    total = check = 0
    for r in range(rounds):
        for nums in arrays:
            longest = max_subarray_length(nums)
            total += longest
            check = (check * 31 + longest + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: lengths total {total}, checksum {check}")


main()
