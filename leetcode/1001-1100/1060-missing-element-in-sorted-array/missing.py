# LeetCode #1060: Missing Element in Sorted Array -- the mirror of the
# ★ arm, missing.kara; its output is byte-identical.


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


def sorted_values(n, first, widest):
    nums = [first]
    for _ in range(1, n):
        gap = 1 + next_random() % widest
        nums.append(nums[-1] + gap)
    return nums


def mix(check, answer):
    return (check * 31 + answer % 1000003) % 1000000007


def show(nums):
    return "[" + ", ".join(str(x) for x in nums) + "]"


def main():
    examples = [
        ([4, 7, 9, 10], 1),
        ([4, 7, 9, 10], 3),
        ([1, 2, 4], 3),
        ([5], 1),
        ([1, 2, 3], 1),
        ([1, 3], 1),
        ([2, 4, 6, 8], 4),
        ([10, 11, 12, 20], 7),
        ([10, 11, 12, 20], 8),
        ([1, 10000000], 100000000),
    ]
    for nums, k in examples:
        print(f"{show(nums)} {k} -> {missing_element(nums, k)}")
    total = check = 0
    for _ in range(3000):
        n = next_random() % 10 + 1
        nums = sorted_values(n, next_random() % 10 + 1, 4)
        k = next_random() % 20 + 1
        answer = missing_element(nums, k)
        total += answer
        check = mix(check, answer)
    print(f"3000 arrays of 1 to 10 values, k to 20: sum {total}, checksum {check}")
    total = check = 0
    for _ in range(3000):
        n = next_random() % 50 + 1
        widest = 1 if next_random() % 2 == 0 else 2
        nums = sorted_values(n, next_random() % 100 + 1, widest)
        k = next_random() % 60 + 1
        answer = missing_element(nums, k)
        total += answer
        check = mix(check, answer)
    print(f"3000 dense arrays of 1 to 50 values, k to 60: sum {total}, checksum {check}")
    total = check = calls = 0
    for a in range(40):
        nums = sorted_values(50000, next_random() % 100 + 1, 2 + a % 300)
        span = nums[-1] - nums[0] - (len(nums) - 1)
        for j in range(10):
            if j < 8:
                k = 1 + next_random() * 32768 % (span + 1000)
            else:
                hi = next_random() * 32768
                k = 1 + (hi + next_random()) % 100000000
            answer = missing_element(nums, k)
            total += answer
            check = mix(check, answer)
            calls += 1
    print(f"40 arrays of 50000 values, {calls} calls: sum {total}, checksum {check}")
    nums = sorted_values(1000, 1, 3)
    total = check = 0
    for k in range(1, 3001):
        answer = missing_element(nums, k)
        total += answer
        check = mix(check, answer)
    print(f"1000 values to {nums[999]}, every k to 3000: sum {total}, checksum {check}")
    run = list(range(1, 50001))
    print(f"1 to 50000, k = 1: {missing_element(run, 1)}, k = 100000000: {missing_element(run, 100000000)}")


main()
