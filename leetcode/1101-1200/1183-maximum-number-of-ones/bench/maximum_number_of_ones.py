# LeetCode #1183: Maximum Number of Ones -- the ★ arm in Python: the cells
# on each position of the side * side square counted, sorted largest
# first, and the first max_ones summed.


def maximum_number_of_ones(width, height, side_length, max_ones):
    counts = []
    for i in range(side_length):
        for j in range(side_length):
            across = (width - i - 1) // side_length + 1
            down = (height - j - 1) // side_length + 1
            counts.append(across * down)
    counts.sort(reverse=True)
    return sum(counts[:max_ones])


def main():
    seed = 1183

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    cases = []
    for _ in range(1000):
        width = 1 + next_random() % 100
        height = 1 + next_random() % 100
        side = 1 + next_random() % min(width, height)
        max_ones = next_random() % (side * side + 1)
        cases.append((width, height, side, max_ones))
    rounds = 100
    check = 0
    for r in range(rounds):
        for width, height, side, max_ones in cases:
            check = (check * 131 + maximum_number_of_ones(width, height, side, max_ones) + r) % 1000000007
    print(f"{rounds} rounds of 1000 cases: checksum {check}")


main()
