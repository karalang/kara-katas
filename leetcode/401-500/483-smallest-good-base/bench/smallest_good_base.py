# Benchmark for #483: Python mirror of the ★ arm (the most 1s first, a
# float root); see smallest_good_base.kara.


def is_ones(n, k, m):
    total = 1
    term = 1
    for _ in range(1, m):
        if term > (n - total) // k:
            return False
        term *= k
        total += term
    return total == n


def smallest_good_base(n):
    value = int(n)
    m = 63
    while m >= 3:
        root = int(float(value) ** (1.0 / (m - 1)))
        for k in range(root, root + 2):
            if k >= 2 and is_ones(value, k, m):
                return f"{k}"
        m -= 1
    return f"{value - 1}"


def main():
    count = 50000
    total = 0
    checksum = 0
    for i in range(count):
        n = 1000000000000000000 - 7 * i
        if i % 3 == 2:
            k = 2 + i // 3
            m = 3 + (i // 3) % 6
            n = 1
            term = 1
            for _ in range(1, m):
                if term > (1000000000000000000 - n) // k:
                    break
                term *= k
                n += term
        base = int(smallest_good_base(f"{n}"))
        total += base % 1000
        checksum = (checksum * 31 + base % 1000000007) % 1000000007
    print(f"{count} values: bases add up to {total} (mod 1000 each), checksum {checksum}")


main()
