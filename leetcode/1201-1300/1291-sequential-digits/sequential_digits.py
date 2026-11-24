# LeetCode #1291: Sequential Digits -- Python mirror of the ★ arm: the 36
# numbers with sequential digits made by length, then first digit.


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

    def show(low, high):
        found = sequential_digits(low, high)
        print(f"low = {low}, high = {high} -> [{', '.join(str(x) for x in found)}]")

    show(100, 300)
    show(1000, 13000)
    show(10, 1000000000)
    show(10, 11)
    show(12, 12)
    show(58, 155)
    show(123456789, 1000000000)
    show(123456790, 1000000000)
    count = 0
    check = 0
    for k in range(20000):
        if k % 3 == 0:
            low = 10 + wide_random() % 999999991
            high = low + wide_random() % (1000000001 - low)
        else:
            base = 10
            for _ in range(next_random() % 8):
                base *= 10
            span = 1
            for _ in range(next_random() % 10):
                span *= 10
            low = base + wide_random() % (9 * base)
            high = low + wide_random() % span
            high = min(high, 1000000000)
        found = sequential_digits(low, high)
        count += len(found)
        for x in found:
            check = (check * 131 + x) % 1000000007
        check = (check * 7 + len(found)) % 1000000007
    print(f"20000 random ranges: {count} numbers, checksum {check}")


main()
