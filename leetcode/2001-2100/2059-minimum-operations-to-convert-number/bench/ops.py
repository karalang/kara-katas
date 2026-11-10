# LeetCode #2059: Minimum Operations to Convert Number -- Python mirror of
# the ★ arm's benchmark (ops.kara): the same 16000 problems, each answered
# by one breadth-first search over the values 0 to 1000.
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
            x = (next_random() * 32768 + next_random()) % 2000000001 - 1000000000
        else:
            x = next_random() % (2 * spread + 1) - spread
        if x not in nums:
            nums.append(x)
    return nums


def main():
    unreachable = total = check = 0
    for _ in range(16000):
        n = next_random() % 16 + 1
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
    print(f"16000 problems: {unreachable} unreachable, sum {total}, checksum {check}")


main()
