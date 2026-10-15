# Benchmark for #660: base 9, read as base 10, as the Kara ★ arm.


def new_integer(n):
    rest, place, out = n, 1, 0
    while rest > 0:
        out += rest % 9 * place
        rest //= 9
        place *= 10
    return out


def main():
    count = 50000000
    checksum = 0
    for i in range(count):
        n = 1 + i * 16
        checksum = (checksum * 31 + new_integer(n)) % 1000000007
    print(f"{count} values of n: checksum {checksum}")


main()
