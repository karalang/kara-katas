# LeetCode #1499: Max Value of Equation -- the bench in Python, mirroring
# find_max_value_of_equation.kara: a window of (y - x, x) kept largest first.
from collections import deque


def find_max_value_of_equation(points, k):
    window = deque()
    best = None
    for x, y in points:
        while window and x - window[0][1] > k:
            window.popleft()
        if window:
            v = window[0][0] + y + x
            if best is None or v > best:
                best = v
        while window and window[-1][0] <= y - x:
            window.pop()
        window.append((y - x, x))
    return best


def main():
    seed = 1499
    points = []
    x = 0
    for _ in range(200000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        x += 1 + seed // 65536 % 10
        seed = (seed * 1103515245 + 12345) % 2147483648
        y = seed // 65536 * 6151 % 200000001 - 100000000
        points.append([x, y])
    check = 0
    for call in range(400):
        at = (check + call * 7919) % 200000
        points[at][1] = (check * 17 + call) % 200000001 - 100000000
        k = 10 + (check + call) % 2000
        check = (check * 31 + find_max_value_of_equation(points, k) + 300000000) % 1000000007
    print(f"400 calls over 200000 points: checksum {check}")


main()
