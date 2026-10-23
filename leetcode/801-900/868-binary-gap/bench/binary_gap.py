# LeetCode #868: Binary Gap -- Python mirror of the bench program (the ★
# arm, one pass over the bits).


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


def main():
    limit = 10000000
    total = 0
    check = 0
    for n in range(1, limit + 1):
        g = binary_gap(n)
        total += g
        check = (check * 31 + g) % 1000000007
    print(f"n from 1 to {limit}: gaps sum to {total}, checksum {check}")


main()
