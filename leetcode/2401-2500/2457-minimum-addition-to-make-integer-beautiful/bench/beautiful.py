# LeetCode #2457: Minimum Addition to Make Integer Beautiful -- bench,
# Python mirror of beautiful.kara: while the digit sum is too large,
# n + x is rounded up to the next multiple of a power of ten one place
# higher.


def digit_sum(x):
    rest = x
    total = 0
    while rest > 0:
        total += rest % 10
        rest //= 10
    return total


def make_integer_beautiful(n, target):
    m = n
    p = 1
    while digit_sum(m) > target:
        p *= 10
        m = (m + p - 1) // p * p
    return m - n


seed = 2457


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    pairs = []
    for _ in range(100000):
        a = next_random()
        b = next_random()
        n = 1 + (a * 1073741824 + b * 32768 + next_random()) % 1000000000000
        pairs.append((n, next_random() % 150))
    check = 0
    for p in range(36):
        for n, t in pairs:
            check = (check * 31 + make_integer_beautiful(n, 1 + (t + p) % 150) + p) % 1000000007
    print(f"36 passes over 10^5 pairs: checksum {check}")


main()
