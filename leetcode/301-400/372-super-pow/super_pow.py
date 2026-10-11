# LeetCode #372: Super Pow -- mirror of super_pow.kara.

MODULUS = 1337


def pow_mod(base, exp):
    out = 1
    for _ in range(exp):
        out = out * base % MODULUS
    return out


def super_pow(a, b):
    base = a % MODULUS
    out = 1
    for d in b:
        out = pow_mod(out, 10) * pow_mod(base, d) % MODULUS
    return out


def show(label, a, b):
    print(f"{label}: {super_pow(a, b)}")


def main():
    show("example 1", 2, [3])
    show("example 2", 2, [1, 0])
    show("example 3", 1, [4, 3, 3, 8, 5, 2])
    show("example 4", 2147483647, [2, 0, 0])
    show("a multiple of 1337", 2674, [5])
    show("one more than 1337", 1338, [9, 9, 9])
    show("a = 7, a factor of 1337", 7, [1, 2, 3, 4])
    show("a = 191, the other factor", 191, [1, 2, 3, 4])
    show("exponent 1", 12345, [1])
    show("2000 nines", 3, [9] * 2000)
    seed = 372
    checksum = 0
    for _ in range(300):
        seed = (seed * 1103515245 + 12345) % 2147483648
        high = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = 1 + (high * 65536 + seed // 32768) % 2147483647
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + (seed // 65536) % 200
        b = []
        for k in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            d = (seed // 65536) % 10
            b.append(1 if k == 0 and d == 0 else d)
        checksum = (checksum * 1337 + super_pow(a, b)) % 1000000007
    print(f"300 random cases: checksum {checksum}")


main()
