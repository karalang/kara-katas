"""LeetCode 233 — Number of Digit One (Python mirror / oracle).

Per-position counting: for each place value, split n into high/cur/low and add
the 1s contributed at that digit. O(log n). Mirrors the Kara version.
"""


def count_digit_one(n):
    if n < 0:
        return 0
    count = 0
    pos = 1
    while pos <= n:
        high = n // (pos * 10)
        cur = (n // pos) % 10
        low = n % pos
        if cur == 0:
            count += high * pos
        elif cur == 1:
            count += high * pos + low + 1
        else:
            count += (high + 1) * pos
        pos *= 10
    return count


def report(n):
    print(count_digit_one(n))


def main():
    report(13)
    report(0)
    report(1)
    report(10)
    report(20)
    report(99)
    report(100)
    report(1024)
    report(999999999)
    report(1000000000)


main()
