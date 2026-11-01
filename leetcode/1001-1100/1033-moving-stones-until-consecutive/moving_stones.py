# LeetCode #1033: Moving Stones Until Consecutive -- by the gaps
# Mirrors moving_stones.kara (the ★ arm) and prints the same output.


def num_moves_stones(a, b, c):
    x, y, z = sorted([a, b, c])
    if z - x == 2:
        fewest = 0
    elif y - x <= 2 or z - y <= 2:
        fewest = 1
    else:
        fewest = 2
    return [fewest, z - x - 2]


seed = 1033


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    examples = [(1, 2, 5), (4, 3, 2), (3, 5, 1), (1, 3, 5), (1, 4, 7), (10, 1, 100), (50, 52, 49), (7, 1, 3)]
    for a, b, c in examples:
        m = num_moves_stones(a, b, c)
        print(f"{a}, {b}, {c} -> [{m[0]},{m[1]}]")
    for top in [6, 20]:
        least = most = check = count = 0
        for a in range(1, top + 1):
            for b in range(1, top + 1):
                for c in range(1, top + 1):
                    if a != b and b != c and a != c:
                        m = num_moves_stones(a, b, c)
                        least += m[0]
                        most += m[1]
                        check = (check * 131 + m[0] * 101 + m[1]) % 1000000007
                        count += 1
        print(f"all {count} orders of three positions from 1 to {top}: minimum sum {least}, maximum sum {most}, checksum {check}")
    least = most = check = count = 0
    while count < 50:
        a = next_random() % 100 + 1
        b = next_random() % 100 + 1
        c = next_random() % 100 + 1
        if a != b and b != c and a != c:
            m = num_moves_stones(a, b, c)
            least += m[0]
            most += m[1]
            check = (check * 131 + m[0] * 101 + m[1]) % 1000000007
            count += 1
    print(f"50 random positions from 1 to 100: minimum sum {least}, maximum sum {most}, checksum {check}")
    for a, b, c in [(1, 50, 100), (1, 2, 100), (1, 99, 100), (98, 99, 100), (100, 1, 3)]:
        m = num_moves_stones(a, b, c)
        print(f"{a}, {b}, {c} -> [{m[0]},{m[1]}]")


main()
