# LeetCode #400: Nth Digit -- mirror of nth_digit.kara (skip whole blocks).


def find_nth_digit(n):
    rest = n
    digits = 1
    count = 9
    start = 1
    while rest > digits * count:
        rest -= digits * count
        digits += 1
        count *= 10
        start *= 10
    number = start + (rest - 1) // digits
    shift = digits - 1 - (rest - 1) % digits
    x = number
    while shift > 0:
        x = x // 10
        shift -= 1
    return x % 10


seed = 400


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for n in [3, 11, 1, 9, 10, 12, 189, 190, 191, 192, 2889, 2890, 1000000000, 2147483647]:
        print(f"{n}: {find_nth_digit(n)}")
    prefix = "".join(str(find_nth_digit(n)) for n in range(1, 61))
    print(f"digits 1 to 60: {prefix}")
    total = 0
    checksum = 0
    for _ in range(3000):
        hi = step()
        n = 1 + (hi * 32768 + step()) % 2147483647
        d = find_nth_digit(n)
        total += d
        checksum = (checksum * 31 + d) % 1000000007
    print(f"3000 random positions: total {total}, checksum {checksum}")


main()
