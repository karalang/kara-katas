# LeetCode #2289: Steps to Make Array Non-decreasing -- the bench, the ★
# arm's Python mirror. A stack of the elements still standing to the
# left, each with the step at which it is removed.


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


# ---- bench harness ---------------------------------------------------------

seed = 2289


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = [[i * 3 + next_random() % 20000 for i in range(10000)] for _ in range(50)]
    check = 0
    for _ in range(20):
        total = 0
        for nums in arrays:
            total += total_steps(nums)
        check = (check * 31 + total) % 1000000007
    print(f"20 passes over 50 arrays of 10^4: checksum {check}")


main()
