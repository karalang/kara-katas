# LeetCode #2832: Maximal Range That Each Element Is Maximum in It --
# the bench, mirrored from ranges.kara: two passes of a falling stack.


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


seed = 2832


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 20, 20, 100000
    arrays = []
    for _ in range(count):
        nums = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            hi = next_random()
            j = (hi * 32768 + next_random()) % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        arrays.append(nums)
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            for x in maximum_length_of_ranges(nums):
                total += x
                check = (check * 31 + x + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: ranges total {total}, checksum {check}")


main()
