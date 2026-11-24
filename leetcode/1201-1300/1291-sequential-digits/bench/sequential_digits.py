# LeetCode #1291 bench: the ★ arm over 10^5 ranges built once, then 20
# passes, each moving every range's low up by the checksum so far, answering
# it, and folding the count and the numbers found into the checksum.


def sequential_digits(low, high):
    found = []
    for length in range(2, 10):
        for first in range(1, 11 - length):
            x = 0
            for d in range(first, first + length):
                x = x * 10 + d
            if low <= x <= high:
                found.append(x)
    return found


def main():
    seed = 1291

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide_random():
        a = next_random()
        return a * 32768 + next_random()

    ranges = []
    for _ in range(100000):
        base = 10
        for _ in range(next_random() % 8):
            base *= 10
        span = 1
        for _ in range(next_random() % 10):
            span *= 10
        low = base + wide_random() % (9 * base)
        high = low + wide_random() % span
        ranges.append((low, min(high, 1000000000)))
    check = 0
    for p in range(20):
        for low, high in ranges:
            moved = low + check % 1000
            found = sequential_digits(min(moved, high), high)
            check = (check * 31 + len(found) + p) % 1000000007
            for x in found:
                check = (check * 131 + x) % 1000000007
    print(f"20 passes over 10^5 ranges: checksum {check}")


main()
