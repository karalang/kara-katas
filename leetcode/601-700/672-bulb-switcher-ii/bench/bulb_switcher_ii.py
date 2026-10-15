# Benchmark for #672: the cases worked out, as the Kara ★ arm.


def flip_lights(n, m):
    if m == 0:
        return 1
    if n == 1:
        return 2
    if n == 2:
        return 3 if m == 1 else 4
    if m == 1:
        return 4
    if m == 2:
        return 7
    return 8


def main():
    count = 100000000
    s = 0
    for i in range(count):
        s = (s * 31 + flip_lights(1 + i % 1000, i // 1000 % 1001)) % 1000000007
    print(f"{count} queries: checksum {s}")


main()
