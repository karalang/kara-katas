# LeetCode #1739: Building Boxes -- the bench (boxes.kara in Python): the
# staircase layer by layer, then the floor a box at a time.


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


count, rounds = 20000, 15
counts = [wide() % 1000000000 + 1 for _ in range(count)]
total = 0
check = 0
for r in range(rounds):
    for n in counts:
        answer = minimum_boxes(n)
        total += answer
        check = (check * 31 + answer + r) % 1000000007
print(f"{count} counts up to 1000000000, {rounds} rounds: floors sum to {total}, checksum {check}")
