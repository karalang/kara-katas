# LeetCode #1739: Building Boxes -- mirrors boxes.kara (the ★ arm).


def minimum_boxes(n):
    placed = 0
    side = 0
    while placed + (side + 1) * (side + 2) // 2 <= n:
        side += 1
        placed += side * (side + 1) // 2
    floor = side * (side + 1) // 2
    extra = 0
    while placed < n:
        extra += 1
        floor += 1
        placed += extra
    return floor


seed = 1739


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
        n = wide() % most + 1
        answer = minimum_boxes(n)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} counts up to {most}: floors sum to {total}, checksum {check}")


for n in [3, 4, 10, 1, 2, 20, 21, 1000000000]:
    print(minimum_boxes(n))
print(f"every count from 1 to 2000: floors sum to {sum(minimum_boxes(n) for n in range(1, 2001))}")
batch(3000, 1000)
batch(3000, 1000000000)
