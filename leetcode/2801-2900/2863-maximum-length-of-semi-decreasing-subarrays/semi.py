# LeetCode #2863: Maximum Length of Semi-Decreasing Subarrays -- the ★
# arm's mirror: the prefix maxima on a stack, the ends walked from the
# right, each start above the end matched with it and popped.


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


seed = 2863


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(f"{max_subarray_length([7, 6, 5, 4, 3, 2, 1, 6, 10, 11])} {max_subarray_length([57, 55, 50, 60, 61, 58, 63, 59, 64, 60, 63])} {max_subarray_length([1, 2, 3, 4])}")
    n = 100000
    print(f"{max_subarray_length([1000000000 - 2 * i for i in range(n)])} {max_subarray_length([2 * i - 1000000000 for i in range(n)])} {max_subarray_length([7] * n)}")
    total = check = 0
    for c in range(3030):
        small = c < 3000
        n = next_random() % 8 + 1 if small else wide() % 90001 + 10000
        if small:
            nums = [next_random() % 6 for _ in range(n)]
        elif c % 2 == 0:
            nums = [wide() % 2000000001 - 1000000000 for _ in range(n)]
        else:
            nums = [20000 * i - 1000000000 for i in range(n)]
        if not small and c % 2 == 1:
            for _ in range(5):
                i = wide() % n
                nums[i] = wide() % 2000000001 - 1000000000
        longest = max_subarray_length(nums)
        total += longest
        check = (check * 31 + longest) % 1000000007
        if c == 2999:
            print(f"3000 short arrays: lengths total {total}, checksum {check}")
            total = check = 0
    print(f"30 long arrays: lengths total {total}, checksum {check}")


main()
