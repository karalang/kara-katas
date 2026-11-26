def check_if_can_break(s1, s2):
    a = sorted(s1.encode())
    b = sorted(s2.encode())
    return all(x >= y for x, y in zip(a, b)) or all(x <= y for x, y in zip(a, b))


def main():
    seed = 1433
    pool = []
    up = []
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        c = 97 + seed // 65536 % 25
        seed = (seed * 1103515245 + 12345) % 2147483648
        pool.append(chr(c))
        up.append(chr(c + seed // 65536 % 2))
    pool = "".join(pool)
    up = "".join(up)
    breaks = 0
    for _ in range(400):
        seed = (seed * 1103515245 + 12345) % 2147483648
        high = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        one = (high * 32768 + seed // 65536) % 900001
        seed = (seed * 1103515245 + 12345) % 2147483648
        if seed // 65536 % 2 == 0:
            got = check_if_can_break(pool[one:one + 100000], up[one:one + 100000])
        else:
            seed = (seed * 1103515245 + 12345) % 2147483648
            high = seed // 65536
            seed = (seed * 1103515245 + 12345) % 2147483648
            two = (high * 32768 + seed // 65536) % 900001
            got = check_if_can_break(pool[one:one + 100000], pool[two:two + 100000])
        if got:
            breaks += 1
    print(f"400 pairs of 10^5 letters: {breaks} can break")


main()
