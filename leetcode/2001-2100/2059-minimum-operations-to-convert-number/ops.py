# LeetCode #2059: Minimum Operations to Convert Number -- Python mirror of
# the ★ arm (ops.kara): a breadth-first search from `start` over the
# values 0 to 1000, each value an operation gives checked against `goal`
# before the range.
from collections import deque


def minimum_operations(nums, start, goal):
    seen = [False] * 1001
    queue = deque()
    seen[start] = True
    queue.append((start, 0))
    while queue:
        x, steps = queue.popleft()
        for n in nums:
            for y in (x + n, x - n, x ^ n):
                if y == goal:
                    return steps + 1
                if 0 <= y <= 1000 and not seen[y]:
                    seen[y] = True
                    queue.append((y, steps + 1))
    return -1


seed = 2059


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, spread):
    nums = []
    while len(nums) < n:
        if next_random() % 8 == 0:
            hi = next_random()
            x = (hi * 32768 + next_random()) % 2000000001 - 1000000000
        else:
            x = next_random() % (2 * spread + 1) - spread
        if x not in nums:
            nums.append(x)
    return nums


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        ([2, 4, 12], 2, 12),
        ([3, 5, 7], 0, -4),
        ([2, 8, 16], 0, 1),
        ([1], 0, 1000),
        ([1000000000], 5, 1000000005),
        ([-1], 3, 2),
        ([7], 1000, 1001),
        ([0, 6], 9, 15),
        ([1024], 1000, 24),
    ]
    for nums, start, goal in examples:
        print(f"{show(nums)}, {start} -> {goal}: {minimum_operations(nums, start, goal)}")
    unreachable = total = check = 0
    for _ in range(400):
        n = next_random() % 8 + 1
        spread = [5, 50, 300, 1500][next_random() % 4]
        nums = draw(n, spread)
        start = next_random() % 1001
        goal = next_random() % 1401 - 200
        if goal == start:
            goal += 1
        ops = minimum_operations(nums, start, goal)
        if ops < 0:
            unreachable += 1
        total += ops
        check = (check * 31 + ops + 2) % 1000000007
    print(f"400 problems: {unreachable} unreachable, sum {total}, checksum {check}")
    unreachable = total = check = 0
    for r in range(4):
        nums = draw(100, [20, 200, 1000, 100000][r])
        start = next_random() % 1001
        goal = [1001, -7, 500, 777777][r]
        ops = minimum_operations(nums, start, goal)
        if ops < 0:
            unreachable += 1
        total += ops
        check = (check * 31 + ops + 2) % 1000000007
    print(f"4 problems of 100 numbers: {unreachable} unreachable, sum {total}, checksum {check}")


main()
