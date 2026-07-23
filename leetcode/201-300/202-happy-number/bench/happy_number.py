"""Benchmark workload for LeetCode #202 — Happy Number (Python; scale lane)."""


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


def main():
    limit = 4000000
    sink = 0
    for i in range(1, limit):
        if is_happy(i):
            sink += 1
    print(sink)


main()
