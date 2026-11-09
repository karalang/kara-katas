# LeetCode #2036: Maximum Alternating Subarray Sum -- the ★ arm in Python,
# the same algorithm and harness as alternating.kara: one pass, the best
# sum of a subarray ending here whose last value is added (`plus`) and
# whose last value is subtracted (`minus`).


def maximum_alternating_subarray_sum(nums):
    plus = nums[0]
    minus = None
    best = plus
    for x in nums[1:]:
        next_plus = x if minus is None else max(x, minus + x)
        minus = plus - x
        plus = next_plus
        best = max(best, plus, minus)
    return best


seed = 2036


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer % 1000000007) % 1000000007


def random_values(n, top):
    nums = []
    for _ in range(n):
        hi = next_random()
        lo = next_random()
        nums.append((hi * 32768 + lo) % (2 * top + 1) - top)
    return nums


def show(nums):
    return "[" + ", ".join(str(v) for v in nums) + "]"


def main():
    examples = [
        [3, -1, 1, 2],
        [2, 2, 2, 2, 2],
        [1],
        [-5],
        [-3, -1, -4],
        [1, 100, 1],
        [5, -5, 5, -5],
        [-100000, 100000, -100000, 100000, -100000],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {maximum_alternating_subarray_sum(nums)}")
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 12 + 1
        top = next_random() % 50 + 1
        answer = maximum_alternating_subarray_sum(random_values(n, top))
        total += answer
        check = mix(check, answer)
    print(f"2000 arrays of up to 12 values: sum {total}, checksum {check}")
    total = 0
    check = 0
    for a in range(4):
        top = [100000, 1000, 100000, 3][a]
        answer = maximum_alternating_subarray_sum(random_values(100000, top))
        total += answer
        check = mix(check, answer)
    print(f"4 arrays of 100000 values: sum {total}, checksum {check}")


main()
