# LeetCode #1499: Max Value of Equation -- the Python mirror of
# find_max_value_of_equation.kara: a deque of the earlier points still
# within k, their y - x falling from front to back.
from collections import deque


def find_max_value_of_equation(points, k):
    window = deque()
    best = -(2**31)
    for x, y in points:
        while window and x - window[0][1] > k:
            window.popleft()
        if window:
            best = max(best, window[0][0] + y + x)
        while window and window[-1][0] <= y - x:
            window.pop()
        window.append((y - x, x))
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_points(n, start, gap, spread):
    points = []
    x = start
    for _ in range(n):
        x += 1 + next_random() % gap
        y = next_random() * 4099 % (2 * spread + 1) - spread
        points.append([x, y])
    return points


def main():
    global seed
    f = find_max_value_of_equation
    print(f"{f([[1, 3], [2, 0], [5, 10], [6, -10]], 1)} {f([[0, 0], [3, 0], [9, 2]], 3)}")
    print(f"{f([[0, 5], [4, 7]], 4)} {f([[0, 10], [1, -50], [2, 10]], 2)} {f([[0, 1], [1, 1], [9, 100]], 2)} {f([[1, -8], [2, -5], [4, -1]], 3)} {f([[-100000000, 100000000], [100000000, 100000000]], 200000000)}")
    seed = 1499
    wide = random_points(100000, -100000000, 2000, 100000000)
    print(f"100000 points: {f(wide, 2000)} {f(wide, 1000000)} {f(wide, 200000000)}")
    check = 0
    for _ in range(3000):
        n = 2 + next_random() % 29
        gap = 1 + next_random() % 6
        k = gap + next_random() % 20
        points = random_points(n, -50, gap, 40)
        check = (check * 31 + f(points, k) + 1000) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
