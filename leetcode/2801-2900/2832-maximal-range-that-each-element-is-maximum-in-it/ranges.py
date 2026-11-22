# LeetCode #2832: Maximal Range That Each Element Is Maximum in It -- the
# Python mirror of the ★ arm: two passes of a falling stack, the nearest
# greater number on each side.


def maximum_length_of_ranges(nums):
    n = len(nums)
    left = [-1] * n
    right = [n] * n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] <= nums[i]:
            stack.pop()
        if stack:
            left[i] = stack[-1]
        stack.append(i)
    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] <= nums[i]:
            stack.pop()
        if stack:
            right[i] = stack[-1]
        stack.append(i)
    return [right[i] - left[i] - 1 for i in range(n)]


# ---- the harness: the same in every arm --------------------------------

seed = 2832


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digest(xs):
    h = 0
    for x in xs:
        h = (h * 131 + x) % 1000000007
    return h


def distinct(n):
    step = 100000 // n
    nums = [i * step + next_random() % step + 1 for i in range(n)]
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    print(show(maximum_length_of_ranges([1, 5, 4, 3, 6])))
    print(show(maximum_length_of_ranges([1, 2, 3, 4, 5])))
    print(show(maximum_length_of_ranges([7])))
    print(show(maximum_length_of_ranges([9, 7, 5, 3, 1])))
    out = maximum_length_of_ranges(distinct(100000))
    print(f"{len(out)} {sum(out)} {digest(out)}")
    check = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        check = (check * 31 + digest(maximum_length_of_ranges(distinct(n)))) % 1000000007
    print(f"3000 short arrays: checksum {check}")
    check = 0
    for _ in range(50):
        n = next_random() % 3000 + 1
        check = (check * 31 + digest(maximum_length_of_ranges(distinct(n)))) % 1000000007
    print(f"50 long arrays: checksum {check}")


main()
