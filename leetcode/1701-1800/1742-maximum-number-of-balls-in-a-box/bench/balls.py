# LeetCode #1742: Maximum Number of Balls in a Box -- the bench
# (balls.kara in Python): a count for every digit sum.


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


count, rounds = 200, 20
ranges = []
for _ in range(count):
    a = wide() % 100000 + 1
    b = wide() % 100000 + 1
    ranges.append((min(a, b), max(a, b)))
total = 0
check = 0
for r in range(rounds):
    for low, high in ranges:
        answer = count_balls(low, high)
        total += answer
        check = (check * 31 + answer + r) % 1000000007
print(f"{count} ranges inside 1 to 100000, {rounds} rounds: largest boxes sum to {total}, checksum {check}")
