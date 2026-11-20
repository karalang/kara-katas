# LeetCode #1742: Maximum Number of Balls in a Box -- mirrors balls.kara
# (the ★ arm).


def count_balls(low_limit, high_limit):
    boxes = [0] * 46
    for ball in range(low_limit, high_limit + 1):
        rest = ball
        total = 0
        while rest > 0:
            total += rest % 10
            rest //= 10
        boxes[total] += 1
    return max(boxes)


seed = 1742


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def batch(count, most):
    total = 0
    check = 0
    for _ in range(count):
        a = wide() % most + 1
        b = wide() % most + 1
        low, high = min(a, b), max(a, b)
        answer = count_balls(low, high)
        total += answer
        check = (check * 31 + answer + low) % 1000000007
    print(f"{count} ranges inside 1 to {most}: largest boxes sum to {total}, checksum {check}")


for low, high in [(1, 10), (5, 15), (19, 28), (1, 1), (1, 100000), (99999, 100000)]:
    print(count_balls(low, high))
batch(3000, 100)
batch(1000, 100000)
