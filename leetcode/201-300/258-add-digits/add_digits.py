"""LeetCode 258 - Add Digits. Python oracle.

Mirrors add_digits.kara algorithm-for-algorithm: peel digits with % 10 and // 10,
repeating while the total is still two digits or more.
"""


def add_digits(num):
    n = num
    while n >= 10:
        s = 0
        while n > 0:
            s += n % 10
            n //= 10
        n = s
    return n


def main():
    for n in [38, 0, 9, 10, 18, 19, 99, 100, 12345, 999999999,
              2147483647, 9223372036854775807]:
        print(f"{n} -> {add_digits(n)}")


if __name__ == "__main__":
    main()
