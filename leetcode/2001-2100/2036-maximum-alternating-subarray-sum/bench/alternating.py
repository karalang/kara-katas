# LeetCode #2036: Maximum Alternating Subarray Sum -- the ★ arm in Python,
# the same algorithm and workload as alternating.kara: the best sum ending
# here on a plus, and the one ending on a minus (None at the first value),
# stepped once per value.


def maximum_alternating_subarray_sum(nums):
    plus = nums[0]
    minus = None
    best = plus
    for x in nums[1:]:
        next_plus = x if minus is None else max(x, minus + x)
        minus = plus - x
        plus = next_plus
        best = max(best, plus)
        if minus is not None:
            best = max(best, minus)
    return best


seed = 2036


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for a in range(4):
        top = [100000, 1000, 100000, 3][a]
        nums = []
        for _ in range(100000):
            hi = next_random()
            lo = next_random()
            nums.append((hi * 32768 + lo) % (2 * top + 1) - top)
        arrays.append(nums)
    calls = 0
    total = 0
    check = 0
    for rnd in range(1000):
        for a in range(4):
            at = (rnd * 7919 + a * 104729) % 100000
            arrays[a][at] = -arrays[a][at]
            answer = maximum_alternating_subarray_sum(arrays[a])
            calls += 1
            total += answer
            check = (check * 31 + answer % 1000000007) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
