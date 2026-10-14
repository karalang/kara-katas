# LeetCode #633: Sum of Square Numbers -- Python mirror of the ★ arm.
#
# Two pointers: `a` from 0 up and `b` from the integer square root of
# `c` down, moving whichever end brings the sum toward `c`.


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


seed = 633


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "true" if v else "false"


for c in [5, 3, 0, 1, 2, 4, 13, 9, 18, 21, 1000000, 2147483646, 2147483647, 2147395600]:
    print(f"c = {c} -> {show(judge_square_sum(c))}")
yes = checksum = 0
for c in range(20001):
    if judge_square_sum(c):
        yes += 1
        checksum = (checksum * 31 + c) % 1000000007
print(f"0 to 20000: {yes} sums of two squares, checksum {checksum}")
yes = checksum = 0
for _ in range(300):
    wide = next_random() * 32768 + next_random()
    c = wide * 2 + next_random() % 2
    if judge_square_sum(c):
        yes += 1
        checksum = (checksum * 31 + c) % 1000000007
print(f"300 random values: {yes} sums of two squares, checksum {checksum}")
