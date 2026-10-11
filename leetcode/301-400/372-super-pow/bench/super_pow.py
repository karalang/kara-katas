# Benchmark for #372 -- mirror of super_pow.kara.

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


def main():
    seed = 372
    checksum = 0
    b = [0] * 2000
    for _ in range(500):
        seed = (seed * 1103515245 + 12345) % 2147483648
        high = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = 1 + (high * 65536 + seed // 32768) % 2147483647
        for k in range(2000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            d = (seed // 65536) % 10
            b[k] = 1 if k == 0 and d == 0 else d
        checksum = (checksum * 1337 + super_pow(a, b)) % 1000000007
    print(f"checksum {checksum}")


main()
