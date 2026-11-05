# LeetCode #1051: Height Checker -- Python mirror of height_checker.kara.
#
# The same check: sort a copy of the line and count the places where the
# two differ.


def height_checker(heights):
    expected = sorted(heights)
    moved = 0
    for i in range(len(heights)):
        if heights[i] != expected[i]:
            moved += 1
    return moved


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_heights(count, tallest):
    return [next_random() % tallest + 1 for _ in range(count)]


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        [1, 1, 4, 2, 1, 3],
        [5, 1, 2, 3, 4],
        [1, 2, 3, 4, 5],
        [7],
        [2, 1],
        [3, 3, 3, 3],
        [5, 4, 3, 2, 1],
        [2, 1, 2, 1, 2],
        [1, 3, 2, 3, 1],
        [100, 1, 100, 1, 50, 50],
    ]
    for heights in examples:
        print(f"{show(heights)} -> {height_checker(heights)}")
    seed = 1051
    total = 0
    check = 0
    for _ in range(3000):
        count = next_random() % 8 + 1
        answer = height_checker(random_heights(count, 4))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"3000 random lines of 1 to 8 students of 1 to 4: total {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(1000):
        count = next_random() % 100 + 1
        answer = height_checker(random_heights(count, 100))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"1000 random lines of 1 to 100 students of 1 to 100: total {total}, checksum {check}")
    falling = [100 - i for i in range(100)]
    print(f"100 students, tallest first -> {height_checker(falling)}")
    swapped = list(range(1, 101))
    swapped[0], swapped[99] = swapped[99], swapped[0]
    print(f"100 students in order, the ends swapped -> {height_checker(swapped)}")


main()
