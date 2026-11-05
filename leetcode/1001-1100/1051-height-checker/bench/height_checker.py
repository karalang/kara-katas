# LeetCode #1051: Height Checker -- Python mirror of
# bench/height_checker.kara.


def height_checker(heights):
    expected = sorted(heights)
    moved = 0
    for i in range(len(heights)):
        if heights[i] != expected[i]:
            moved += 1
    return moved


seed = 1051


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lines, count, rounds = 2000, 100, 50
    all_lines = [[next_random() % 100 + 1 for _ in range(count)] for _ in range(lines)]
    total = 0
    check = 0
    for _ in range(rounds):
        for heights in all_lines:
            answer = height_checker(heights)
            total += answer
            check = (check * 131 + answer) % 1000000007
    print(f"{lines} lines of {count} students, {rounds} rounds: total {total}, checksum {check}")


main()
