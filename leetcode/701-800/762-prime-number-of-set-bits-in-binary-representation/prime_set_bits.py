# LeetCode 762 — Prime Number of Set Bits in Binary Representation: the
# ★ arm in Python, same output.


def count_prime_set_bits(left, right):
    count = 0
    for n in range(left, right + 1):
        bits = 0
        rest = n
        while rest > 0:
            rest &= rest - 1
            bits += 1
        if bits in (2, 3, 5, 7, 11, 13, 17, 19):
            count += 1
    return count


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def show(left, right):
    print(f"[{left}, {right}] -> {count_prime_set_bits(left, right)}")


def main():
    global seed
    for left, right in [(6, 10), (10, 15), (1, 1), (3, 3), (1, 10000),
                        (990000, 1000000), (524287, 524288)]:
        show(left, right)
    seed = 762
    total = 0
    check = 0
    for _ in range(300):
        left = 1 + wide_random() % 1000000
        right = left + wide_random() % 10001
        count = count_prime_set_bits(left, right)
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"300 random ranges: {total} numbers counted, checksum {check}")


main()
