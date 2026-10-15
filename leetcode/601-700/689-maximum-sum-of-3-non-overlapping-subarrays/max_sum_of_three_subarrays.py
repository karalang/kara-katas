# LeetCode #689: Maximum Sum of 3 Non-Overlapping Subarrays -- best to
# each side.
#
# A mirror of max_sum_of_three_subarrays.kara (the ★ arm) and its harness.


def max_sum_of_three_subarrays(nums, k):
    n = len(nums)
    count = n - k + 1
    w = [0] * count
    s = 0
    for i in range(n):
        s += nums[i]
        if i >= k:
            s -= nums[i - k]
        if i >= k - 1:
            w[i - k + 1] = s
    left = [0] * count
    best = 0
    for i in range(count):
        if w[i] > w[best]:
            best = i
        left[i] = best
    right = [0] * count
    best = count - 1
    for i in range(count - 1, -1, -1):
        if w[i] >= w[best]:
            best = i
        right[i] = best
    answer = []
    top = -1
    for j in range(k, count - k):
        a = left[j - k]
        c = right[j + k]
        total = w[a] + w[j] + w[c]
        if total > top:
            top = total
            answer = [a, j, c]
    return answer


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(nums, k):
    text = ",".join(str(x) for x in nums)
    print(f"[{text}], k = {k} -> {max_sum_of_three_subarrays(nums, k)}")


def main():
    show([1, 2, 1, 2, 6, 7, 5, 1], 2)
    show([1, 2, 1, 2, 1, 2, 1, 2, 1], 2)
    show([4, 9, 1], 1)
    show([3] * 11, 3)
    show([1, 3, 2, 4, 1, 5], 1)
    show([5, 1, 5, 1, 5, 1, 5], 1)
    show([1, 5, 5, 1, 1, 1, 1], 2)
    show([65535] * 6, 2)

    queries = 0
    checksum = 0
    for n in range(3, 9):
        for code in range(3 ** n):
            nums = []
            c = code
            for _ in range(n):
                nums.append(1 + c % 3)
                c //= 3
            for k in range(1, n // 3 + 1):
                got = max_sum_of_three_subarrays(nums, k)
                queries += 1
                checksum = (checksum * 31 + got[0] * 64 + got[1] * 8 + got[2]) % 1000000007
    print(f"{queries} small queries: checksum {checksum}")

    seed = [689]
    checksum = 0
    for _ in range(300):
        n = 3 + next_random(seed) % 298
        k = 1 + next_random(seed) % (n // 3)
        nums = [1 + next_random(seed) % 65535 for _ in range(n)]
        got = max_sum_of_three_subarrays(nums, k)
        checksum = (checksum * 31 + got[0] * 90000 + got[1] * 300 + got[2]) % 1000000007
    print(f"300 random arrays: checksum {checksum}")

    big = [1 + next_random(seed) % 65535 for _ in range(2000)]
    line = ""
    for k in [1, 10, 100, 500, 666]:
        if k != 1:
            line += ";"
        line += f" k = {k}: {max_sum_of_three_subarrays(big, k)}"
    print(f"2000 random values:{line}")
    print(f"2000 ones, k = 7: {max_sum_of_three_subarrays([1] * 2000, 7)}")


main()
