# LeetCode #699: Falling Squares -- every earlier square checked.
#
# A mirror of falling_squares.kara (the ★ arm) and its harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def falling_squares(positions):
    tops = []
    answer = []
    highest = 0
    for i, (left, side) in enumerate(positions):
        base = 0
        for j in range(i):
            other, other_side = positions[j]
            if left < other + other_side and other < left + side:
                base = max(base, tops[j])
        top = base + side
        tops.append(top)
        highest = max(highest, top)
        answer.append(highest)
    return answer


def show(h):
    return "[" + ", ".join(str(x) for x in h) + "]"


def main():
    global seed
    f = falling_squares
    print(f"example 1: {show(f([(1, 2), (2, 3), (6, 1)]))}")
    print(f"example 2: {show(f([(100, 100), (200, 100)]))}")
    print(f"one: {show(f([(5, 7)]))}")
    print(f"touching: {show(f([(1, 2), (3, 2), (5, 2), (0, 1)]))}")
    print(f"stacked: {show(f([(5, 3), (5, 3), (5, 3), (5, 3)]))}")
    print(f"bridge: {show(f([(1, 2), (9, 5), (0, 20), (4, 1), (19, 1), (20, 1)]))}")
    stair = [(1 + i * 99999, 100000) for i in range(1000)]
    row = [(100000000 - i * 1000000, 1000000) for i in range(1000)]
    print(f"stair of 1000: last {f(stair)[999]}, row of 1000: last {f(row)[999]}")
    seed = 699
    total = 0
    checksum = 0
    for _ in range(40):
        n = 1 + next_random() % 1000
        a = next_random() % 2000
        width = 1 + a * (1 + next_random() % 50000)
        biggest = 1 + next_random() % 1000
        positions = []
        for _ in range(n):
            left = 1 + (next_random() * 32768 + next_random()) % width
            side = 1 + next_random() % biggest
            positions.append((left, side))
        for h in f(positions):
            total += h
            checksum = (checksum * 31 + h) % 1000000007
    print(f"40 random problems: heights sum to {total}, checksum {checksum}")


main()
