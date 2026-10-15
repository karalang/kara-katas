# LeetCode #689: Maximum Sum of 3 Non-Overlapping Subarrays -- best to
# each side. Bench.
#
# 100 arrays of 20,000 values from 1 to 65535, each with a k from 1 to
# 1,000, are built once; then 20 rounds answer every array.


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


seed = 689


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 100
    rounds = 20
    arrays = []
    ks = []
    for _ in range(count):
        arrays.append([1 + next_random() % 65535 for _ in range(20000)])
        ks.append(1 + next_random() % 1000)
    total = 0
    for r in range(rounds):
        for c in range(count):
            got = max_sum_of_three_subarrays(arrays[c], ks[c])
            total = (total * 31 + got[0] + got[1] + got[2] + r) % 1000000007
    print(f"{count * rounds} arrays answered, checksum {total}")


main()
