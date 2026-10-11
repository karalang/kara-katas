# Benchmark for #365 -- mirror of water_jug.kara.


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def can_measure_water(x, y, target):
    return target <= x + y and target % gcd(x, y) == 0


def main():
    seed = 365
    yes = 0
    checksum = 0
    for i in range(5000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        x = 1 + (seed // 65536) % 1000000
        seed = (seed * 1103515245 + 12345) % 2147483648
        y = 1 + (seed // 65536) % 1000000
        seed = (seed * 1103515245 + 12345) % 2147483648
        target = ((seed // 65536) % 1000) * (1 + i % 6)
        if can_measure_water(x, y, target):
            yes += 1
            checksum = (checksum * 31 + i) % 1000000007
    print(f"{yes} measurable, checksum {checksum}")


main()
