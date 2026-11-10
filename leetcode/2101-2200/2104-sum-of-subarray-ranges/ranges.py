# LeetCode #2104: Sum of Subarray Ranges -- Python mirror of the ★ arm
# (ranges.kara): each number's share as the largest of its subarrays,
# from a falling stack of places, less its share as the smallest, from a
# rising one. Prints the same lines.


def sub_array_ranges(nums):
    n = len(nums)
    total = 0
    stack = []
    for i in range(n + 1):
        while stack and (i == n or nums[stack[-1]] < nums[i]):
            top = stack.pop()
            left = stack[-1] if stack else -1
            total += nums[top] * (top - left) * (i - top)
        stack.append(i)
    stack.clear()
    for i in range(n + 1):
        while stack and (i == n or nums[stack[-1]] > nums[i]):
            top = stack.pop()
            left = stack[-1] if stack else -1
            total -= nums[top] * (top - left) * (i - top)
        stack.append(i)
    return total


seed = 2104


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def show(nums):
    return "[" + ", ".join(str(x) for x in nums) + "]"


def main():
    examples = [
        [1, 2, 3],
        [1, 3, 3],
        [4, -2, -3, 4, 1],
        [5],
        [7, 7, 7, 7],
        [-1000000000, 1000000000],
        [3, 1, 1, 1, 3],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {sub_array_ranges(nums)}")
    total = 0
    check = 0
    for rnd in range(3000):
        n = next_random() % 60 + 1
        nums = []
        for _ in range(n):
            if rnd % 2 == 0:
                nums.append(next_random() % 41 - 20)
            else:
                nums.append(wide_random() % 2000000001 - 1000000000)
        got = sub_array_ranges(nums)
        total += got % 1000000007
        check = (check * 31 + got % 1000000007 + 1000000007) % 1000000007
    print(f"3000 arrays: total {total}, checksum {check}")
    rising = [i * 2000000 - 1000000000 for i in range(1000)]
    alternating = [1000000000 if i % 2 == 0 else -1000000000 for i in range(1000)]
    spread = [wide_random() % 2000000001 - 1000000000 for _ in range(1000)]
    print(f"rising -> {sub_array_ranges(rising)}")
    print(f"alternating -> {sub_array_ranges(alternating)}")
    print(f"spread -> {sub_array_ranges(spread)}")


main()
