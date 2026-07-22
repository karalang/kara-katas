"""LeetCode 202 — Happy Number (Python mirror / oracle).

Floyd's tortoise-and-hare over the sum-of-squared-digits map; happy iff the fast
pointer reaches 1. Mirrors the Kāra version.
"""


def sq_digit_sum(n):
    total = 0
    x = n
    while x > 0:
        d = x % 10
        total += d * d
        x //= 10
    return total


def is_happy(n):
    slow = n
    fast = sq_digit_sum(n)
    while fast != 1 and slow != fast:
        slow = sq_digit_sum(slow)
        fast = sq_digit_sum(sq_digit_sum(fast))
    return fast == 1


def report(n):
    print("true" if is_happy(n) else "false")


def main():
    report(19)
    report(2)
    report(1)
    report(7)
    report(4)
    report(100)
    report(1111111)


main()
