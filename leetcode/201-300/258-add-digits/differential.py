"""LeetCode 258 - differential harness. Python oracle.

Mirrors differential.kara exactly: the same exhaustive sweep, the same three
forms, the same digest and the same high-range spot check.

Python's % returns non-negative where Kara's keeps the dividend's sign, but the
inputs here are all non-negative so the two agree throughout -- and the closed
form's zero case is an explicit branch precisely so the sign rule never has to
be reasoned about.
"""


def add_digits_loop(num):
    n = num
    while n >= 10:
        s = 0
        while n > 0:
            s += n % 10
            n //= 10
        n = s
    return n


def add_digits_formula(num):
    if num == 0:
        return 0
    return 1 + (num - 1) % 9


def digit_sum_via_text(n):
    return sum(b - 48 for b in str(n).encode())


def add_digits_bytes(num):
    n = num
    while n >= 10:
        n = digit_sum_via_text(n)
    return n


def main():
    hi = 300000
    mismatches = nines = zeros = digest = 0

    for n in range(hi + 1):
        a = add_digits_loop(n)
        b = add_digits_formula(n)
        c = add_digits_bytes(n)
        if a != b or a != c:
            mismatches += 1
        if a == 9:
            nines += 1
        if a == 0:
            zeros += 1
        digest = (digest * 131 + a) % 1000000007

    big = 9223372036854775807
    big_mismatch = 0
    for _ in range(500):
        a = add_digits_loop(big)
        b = add_digits_formula(big)
        c = add_digits_bytes(big)
        if a != b or a != c:
            big_mismatch += 1
        digest = (digest * 131 + a) % 1000000007
        big -= 7919

    print(f"swept 0..{hi}")
    print(f"answer==9 {nines}")
    print(f"answer==0 {zeros}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")
    print(f"high-range mismatches {big_mismatch}")


if __name__ == "__main__":
    main()
