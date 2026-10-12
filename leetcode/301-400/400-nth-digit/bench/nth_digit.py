# Benchmark for #400: mirror of nth_digit.kara (skip whole blocks).
import sys


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


seed = 4001


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    calls = int(sys.argv[1]) if len(sys.argv) > 1 else 10000000
    total = 0
    checksum = 0
    for _ in range(calls):
        hi = step()
        n = 1 + (hi * 32768 + step()) % 2147483647
        d = find_nth_digit(n)
        total += d
        checksum = (checksum * 31 + d) % 1000000007
    print(f"{calls} calls: total {total}, checksum {checksum}")


main()
