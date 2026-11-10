# LeetCode #2090: K Radius Subarray Averages -- Python mirror of the ★ arm's
# benchmark (averages.kara): the same 30 arrays, each asked for the same 10
# radii, one slide of the window into a fresh `list` each.

seed = 2090


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def get_averages(nums, k):
    n = len(nums)
    width = 2 * k + 1
    avgs = [-1] * n
    total = 0
    for i in range(n):
        total += nums[i]
        if i >= width:
            total -= nums[i - width]
        if i + 1 >= width:
            avgs[i - k] = total // width
    return avgs


def main():
    arrays = [[next_random() % 100001 for _ in range(100000)] for _ in range(30)]
    radii = [0, 1, 3, 10, 30, 100, 300, 1000, 3000, 20000]
    total = check = 0
    for nums in arrays:
        for k in radii:
            s = sum(get_averages(nums, k))
            total += s
            check = (check * 31 + s) % 1000000007
    print(f"300 answers: sum {total}, checksum {check}")


main()
