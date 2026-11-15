# LeetCode #2165: Smallest Value of the Rearranged Number -- the Python
# mirror of smallest.kara, the ★ arm: the digits falling below zero, else
# rising with the first digit other than 0 swapped to the front.


def smallest_number(num):
    digits = [int(c) for c in str(abs(num))]
    if num < 0:
        digits.sort(reverse=True)
    else:
        digits.sort()
        for i, d in enumerate(digits):
            if d != 0:
                digits[0], digits[i] = digits[i], digits[0]
                break
    size = 0
    for d in digits:
        size = size * 10 + d
    return -size if num < 0 else size


def rem(a, m):
    # Kāra's `%`, whose sign is the dividend's
    r = abs(a) % m
    return -r if a < 0 else r


seed = 2165


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(num):
    print(f"{num} -> {smallest_number(num)}")


def main():
    for n in [310, -7605, 0, -1000000000000000, 1000000000000000, 1020, -8, -10]:
        show(n)
    total = 0
    check = 0
    M = 1000000007
    for rnd in range(2000):
        length = next_random() % 15 + 1
        top = [2, 5, 10][rnd % 3]
        num = 0
        for _ in range(length):
            num = num * 10 + next_random() % top
        if next_random() % 2 == 1:
            num = -num
        s = smallest_number(num)
        total += rem(s, M)
        check = rem(check * 31 + rem(s, M) + M, M)
    print(f"2000 numbers: {total} in all, checksum {check}")
    every = 0
    for start in range(10):
        num = 0
        for k in range(10):
            num = num * 10 + (start + k) % 10
        every = rem(every * 31 + rem(smallest_number(num), M) + M, M)
        every = rem(every * 31 + rem(smallest_number(-num), M) + M, M)
    print(f"20 rotations: checksum {every}")


main()
