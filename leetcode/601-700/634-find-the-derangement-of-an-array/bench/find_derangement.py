# LeetCode 634 -- Find the Derangement of An Array, bench mirror in
# Python.
#
# The ★ arm of find_derangement.kara: D(n) = (n - 1) * (D(n - 1) +
# D(n - 2)) modulo 10^9 + 7, kept in two variables. Same values of n,
# same output line.
MOD = 1000000007


def find_derangement(n):
    before, last = 1, 0
    for i in range(2, n + 1):
        before, last = last, (i - 1) * ((last + before) % MOD) % MOD
    return last


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [634]
    sizes = []
    for _ in range(100):
        wide = next_random(seed) * 32768 + next_random(seed)
        sizes.append(1 + wide % 1000000)
    total = checksum = 0
    for n in sizes:
        d = find_derangement(n)
        total = (total + d) % MOD
        checksum = (checksum * 31 + d) % MOD
    print(f"{len(sizes)} values of n: total {total}, checksum {checksum}")


main()
