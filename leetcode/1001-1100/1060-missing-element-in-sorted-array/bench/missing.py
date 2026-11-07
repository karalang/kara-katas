# LeetCode #1060: Missing Element in Sorted Array -- the benchmark, the
# same algorithm as missing.kara.


def missing_element(nums, k):
    def missing(i):
        return nums[i] - nums[0] - i

    last = len(nums) - 1
    if missing(last) < k:
        return nums[last] + k - missing(last)
    lo, hi = 0, last
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if missing(mid) < k:
            lo = mid
        else:
            hi = mid
    return nums[lo] + k - missing(lo)


seed = 1060


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    calls = total = check = 0
    for a in range(50):
        nums = [next_random() % 100 + 1]
        for _ in range(1, 50000):
            gap = 1 + next_random() % (2 + a * 3)
            nums.append(nums[-1] + gap)
        span = nums[49999] - nums[0] - 49999
        for _ in range(200000):
            hi = next_random() * 32768
            k = 1 + (hi + next_random()) % (span + 1000)
            answer = missing_element(nums, k)
            total += answer
            check = (check * 31 + answer % 1000003) % 1000000007
            calls += 1
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
