# LeetCode 633 -- Sum of Square Numbers, bench mirror in Python.
#
# The ★ arm of judge_square_sum.kara: two pointers from 0 and from the
# integer square root of `c`, found by binary search. Same values, same
# output line.


def root(n):
    lo, hi = 0, min(n, 3037000499) + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo


def judge_square_sum(c):
    a, b = 0, root(c)
    while a <= b:
        s = a * a + b * b
        if s == c:
            return True
        if s < c:
            a += 1
        else:
            b -= 1
    return False


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [633]
    values = []
    for _ in range(10000):
        wide = next_random(seed) * 32768 + next_random(seed)
        values.append(wide * 2 + next_random(seed) % 2)
    yes = checksum = 0
    for c in values:
        if judge_square_sum(c):
            yes += 1
            checksum = (checksum * 31 + c) % 1000000007
    print(f"{len(values)} values: {yes} sums of two squares, checksum {checksum}")


main()
