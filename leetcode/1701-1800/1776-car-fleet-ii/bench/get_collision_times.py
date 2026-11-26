# LeetCode #1776: Car Fleet II -- the bench in Python, mirroring
# get_collision_times.kara: a stack of the cars ahead from the right.
import math


def catch_time(cars, i, j):
    return (cars[j][0] - cars[i][0]) / (cars[i][1] - cars[j][1])


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


seed = 1776


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    for l in range(20):
        fastest = 1000000 if l % 2 == 0 else 100
        cars = []
        position = 0
        for _ in range(100000):
            position += 1 + next_random() % 10
            speed = 1 + next_random() % fastest
            cars.append([position, speed])
        lists.append(cars)
    check = 0
    for call in range(200):
        answer = get_collision_times(lists[(check + call) % 20])
        t = answer[check % 100000]
        check = (check * 31 + math.floor(t * 100000.0 + 0.5) + 100001) % 1000000007
    print(f"200 calls over 20 lists: checksum {check}")


main()
