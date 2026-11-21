# LeetCode #2523: Closest Prime Numbers in Range -- benchmark mirror of the
# ★ arm (closest.kara): the same queries, each answered by a fresh sieve.


def closest_primes(left, right):
    composite = [False] * (right + 1)
    p = 2
    while p * p <= right:
        if not composite[p]:
            m = p * p
            while m <= right:
                composite[m] = True
                m += p
        p += 1
    best = (-1, -1)
    last = -1
    for x in range(max(left, 2), right + 1):
        if not composite[x]:
            if last != -1 and (best[0] == -1 or x - last < best[1] - best[0]):
                best = (last, x)
            last = x
    return best


def main():
    queries = 150
    check = 0
    for q in range(queries):
        right = check % 500000 + 500001
        a, b = closest_primes(right - 10000, right)
        check = (check * 31 + a + q) % 1000000007
        check = (check * 31 + b) % 1000000007
    print(f"{queries} queries to 10^6: checksum {check}")


main()
