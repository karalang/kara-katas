# LeetCode #962: Maximum Width Ramp -- decreasing stack.
#
# Mirrors max_width_ramp.kara: the prefix minima form a stack of falling
# numbers; right ends walked from the last place back pop every top they
# reach, each popped pair the widest ramp from that top.


def max_width_ramp(nums):
    n = len(nums)
    stack = []
    for i in range(n):
        if not stack or nums[i] < nums[stack[-1]]:
            stack.append(i)
    best = 0
    j = n - 1
    while j >= 0 and stack:
        while stack and nums[stack[-1]] <= nums[j]:
            best = max(best, j - stack[-1])
            stack.pop()
        j -= 1
    return best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, top):
    return [next_random() % (top + 1) for _ in range(n)]


def show(nums):
    return "[" + ",".join(str(x) for x in nums) + "]"


def main():
    global seed
    cases = [
        [6, 0, 8, 2, 1, 5],
        [9, 8, 1, 0, 1, 9, 4, 0, 4, 1],
        [1, 0],
        [0, 1],
        [5, 5],
        [3, 2, 1],
        [1, 2, 3],
        [0, 0, 0, 0],
        [4, 3, 2, 1, 5],
        [2, 9, 1, 3, 0],
        [50000, 0, 0, 50000],
    ]
    for nums in cases:
        print(f"{show(nums)}: {max_width_ramp(nums)}")
    seed = 962
    count = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 2 + next_random() % 19
        top = 1 + next_random() % 9
        nums = random_nums(n, top)
        w = max_width_ramp(nums)
        count += n
        total += w
        check = (check * 31 + w) % 1000000007
    print(f"300 random cases of {count} numbers: the ramps sum to {total}, checksum {check}")
    big = random_nums(50000, 50000)
    print(f"50000 random numbers: {max_width_ramp(big)}")
    down = [50000 - i for i in range(50000)]
    up = list(range(50000))
    valley = [50000 - 2 * i if i < 25000 else 2 * i - 49999 for i in range(50000)]
    zigzag = [50000 - i if i % 2 == 0 else i for i in range(50000)]
    print(f"falling from 50000: {max_width_ramp(down)}")
    print(f"rising from 0: {max_width_ramp(up)}")
    print(f"falling then rising: {max_width_ramp(valley)}")
    print(f"falling and rising in turn: {max_width_ramp(zigzag)}")
    print(f"50000 sevens: {max_width_ramp([7] * 50000)}")
    down[49999] = 50000
    print(f"falling, then 50000 at the end: {max_width_ramp(down)}")


main()
