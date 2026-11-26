# LeetCode #1776: Car Fleet II -- a Python mirror of the ★ arm: a stack of
# the cars ahead, a car popped when it is no slower or joins its own fleet
# before this car could reach it.
import math


def catch_time(cars, i, j):
    return float(cars[j][0] - cars[i][0]) / float(cars[i][1] - cars[j][1])


def get_collision_times(cars):
    n = len(cars)
    answer = [-1.0] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack:
            j = stack[-1]
            if cars[i][1] <= cars[j][1] or (answer[j] > 0.0 and catch_time(cars, i, j) >= answer[j]):
                stack.pop()
            else:
                break
        if stack:
            answer[i] = catch_time(cars, i, stack[-1])
        stack.append(i)
    return answer


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_cars(n, gap, fastest):
    cars = []
    position = 0
    for _ in range(n):
        position += 1 + next_random() % gap
        speed = 1 + next_random() % fastest
        cars.append([position, speed])
    return cars


def show(answer):
    return "[" + ", ".join(f"{t:.5f}" for t in answer) + "]"


def digest(answer):
    check = 0
    for t in answer:
        check = (check * 31 + math.floor(t * 100000.0 + 0.5) + 100001) % 1000000007
    return check


def main():
    global seed
    # LeetCode's two examples
    print(f"{show(get_collision_times([[1, 2], [2, 1], [4, 3], [7, 2]]))} {show(get_collision_times([[3, 4], [5, 4], [6, 3], [9, 1]]))}")
    # the edges
    print(f"{show(get_collision_times([[5, 9]]))} {show(get_collision_times([[1, 3], [4, 3]]))} {show(get_collision_times([[0, 2], [1, 1]]))} {show(get_collision_times([[0, 3], [2, 2], [3, 1]]))} {show(get_collision_times([[0, 4], [1, 3], [2, 2], [3, 1]]))}")
    # the constraints' most
    seed = 1776
    wide = random_cars(100000, 10, 1000000)
    steps = [[i + 1, 100000 - i] for i in range(100000)]
    print(f"the most: {digest(get_collision_times(wide))} {digest(get_collision_times(steps))}")
    # 3000 random cases
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        gap = 1 + next_random() % 10
        fastest = 1 + next_random() % 10
        cars = random_cars(n, gap, fastest)
        check = (check * 31 + digest(get_collision_times(cars))) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
