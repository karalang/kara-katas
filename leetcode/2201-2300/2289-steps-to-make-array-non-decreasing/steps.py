# LeetCode #2289: Steps to Make Array Non-decreasing -- the ★ arm's
# Python mirror. A stack of the elements still standing to the left, each
# with the step at which it is removed.


def total_steps(nums):
    stack = []
    most = 0
    for x in nums:
        step = 0
        while stack and stack[-1][0] <= x:
            step = max(step, stack[-1][1])
            stack.pop()
        step = 0 if not stack else step + 1
        most = max(most, step)
        stack.append((x, step))
    return most


# ---- test harness ---------------------------------------------------------

seed = 2289


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        [5, 3, 4, 4, 7, 3, 6, 11, 8, 5, 11],
        [4, 5, 7, 7, 13],
        [1],
        [7, 7, 7, 7],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [10, 1, 2, 3, 4, 5, 6, 1, 2, 3],
        [5, 4, 3, 6, 5, 4, 7, 6, 5, 8, 1],
    ]
    cases.append([1000000000] + list(range(1, 2000)))
    for nums in cases:
        print(f"{len(nums)} elements: {total_steps(nums)}")
    check = 0
    total = 0
    for _ in range(3000):
        n = next_random() % 60 + 1
        top = next_random() % 50 + 1
        nums = [next_random() % top + 1 for _ in range(n)]
        steps = total_steps(nums)
        check = (check * 31 + steps) % 1000000007
        total += steps
    print(f"3000 arrays: checksum {check}, {total} steps")


main()
