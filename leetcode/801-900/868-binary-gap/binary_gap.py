# LeetCode #868: Binary Gap -- Python mirror of the ★ arm (one pass over
# the bits).


def binary_gap(n):
    best = 0
    last = -1
    rest = n
    position = 0
    while rest > 0:
        if rest % 2 == 1:
            if last >= 0:
                best = max(best, position - last)
            last = position
        rest //= 2
        position += 1
    return best


seed = 868


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_n():
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % 1000000000 + 1


def show(n):
    print(f"n = {n} ({n:b}) -> {binary_gap(n)}")


def main():
    show(22)
    show(8)
    show(5)
    for n in [1, 3, 6, 7, 9, 1041, 529, 20, 15, 32, 805306369, 1000000000, 536870913, 999999999]:
        show(n)
    total = 0
    check = 0
    most = 0
    for n in range(1, 100001):
        g = binary_gap(n)
        total += g
        check = (check * 31 + g) % 1000000007
        most = max(most, g)
    print(f"n from 1 to 100000: gaps sum to {total}, largest {most}, checksum {check}")
    total = 0
    check = 0
    counts = [0] * 31
    for _ in range(100000):
        g = binary_gap(random_n())
        total += g
        check = (check * 31 + g) % 1000000007
        counts[g] += 1
    spread = [f"{g}:{counts[g]}" for g in range(31) if counts[g] > 0]
    print(f"100000 random n up to 10^9: gaps sum to {total}, checksum {check}")
    print(f"gaps by length: {' '.join(spread)}")


main()
