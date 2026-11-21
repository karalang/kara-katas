# LeetCode #2523: Closest Prime Numbers in Range -- Python mirror of the ★
# arm (closest.kara): a sieve to right, then one walk keeping the last prime;
# the same harness and output.


def closest_primes(left, right):
    composite = [False] * (right + 1)
    p = 2
    while p * p <= right:
        if not composite[p]:
            for m in range(p * p, right + 1, p):
                composite[m] = True
        p += 1
    best = (-1, -1)
    last = -1
    for x in range(max(left, 2), right + 1):
        if not composite[x]:
            if last != -1 and (best[0] == -1 or x - last < best[1] - best[0]):
                best = (last, x)
            last = x
    return best


seed = 2523


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def main():
    for left, right in [(10, 19), (4, 6), (1, 1), (1, 2), (2, 3), (1, 10), (14, 16), (89, 97), (1000000, 1000000), (999900, 1000000)]:
        a, b = closest_primes(left, right)
        print(f"{left} {right} -> [{a}, {b}]")
    for count, top, width in [(2000, 10000, 100), (30, 1000000, 10000)]:
        none = 0
        gaps = 0
        check = 0
        for _ in range(count):
            left = wide_random() % top + 1
            right = min(left + wide_random() % width, top)
            a, b = closest_primes(left, right)
            if a == -1:
                none += 1
            else:
                gaps += b - a
            check = (check * 31 + a + 1) % 1000000007
        print(f"{count} random ranges to {top}: {none} with no pair, gaps {gaps}, checksum {check}")
    a, b = closest_primes(1, 1000000)
    print(f"1 1000000 -> [{a}, {b}]")


main()
