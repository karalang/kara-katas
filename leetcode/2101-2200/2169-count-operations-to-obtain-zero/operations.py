# LeetCode #2169: Count Operations to Obtain Zero -- the Python mirror of
# operations.kara: Euclid's algorithm, each round counting a // b
# operations at once.


def count_operations(num1, num2):
    a, b = max(num1, num2), min(num1, num2)
    ops = 0
    while b > 0:
        ops += a // b
        a, b = b, a % b
    return ops


# ---- test harness ---------------------------------------------------------

seed = 2169


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(num1, num2):
    print(f"({num1}, {num2}) -> {count_operations(num1, num2)}")


def main():
    show(2, 3)
    show(10, 10)
    show(0, 0)
    show(0, 7)
    show(5, 5)
    show(1, 100000)
    show(100000, 1)
    show(75025, 46368)
    total = 0
    check = 0
    for rnd in range(2000):
        top = [11, 1001, 100001][rnd % 3]
        pair = [0, 0]
        for k in range(2):
            if next_random() % 10 > 0:
                pair[k] = (next_random() * 32768 + next_random()) % top
        ops = count_operations(pair[0], pair[1])
        total += ops
        check = (check * 31 + ops) % 1000000007
    print(f"2000 pairs: {total} in all, checksum {check}")
    every = 0
    for a in range(301):
        for b in range(301):
            every = (every * 31 + count_operations(a, b)) % 1000000007
    print(f"90601 pairs up to 300: checksum {every}")


main()
