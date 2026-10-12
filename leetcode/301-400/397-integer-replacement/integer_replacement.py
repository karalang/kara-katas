# LeetCode #397: Integer Replacement -- mirror of integer_replacement.kara
# (greedy on the last two bits).


def integer_replacement(n):
    v = n
    ops = 0
    while v != 1:
        if v % 2 == 0:
            v = v // 2
        elif v == 3 or v % 4 == 1:
            v -= 1
        else:
            v += 1
        ops += 1
    return ops


seed = 397


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(n):
    print(f"{n}: {integer_replacement(n)}")


def main():
    for n in [8, 7, 4, 1, 2, 3, 15, 65535, 1073741824, 2147483647]:
        show(n)
    total = 0
    checksum = 0
    for _ in range(3000):
        hi = step()
        n = 1 + (hi * 32768 + step()) % 2147483647
        r = integer_replacement(n)
        total += r
        checksum = (checksum * 31 + r) % 1000000007
    print(f"3000 random values: total {total}, checksum {checksum}")


main()
