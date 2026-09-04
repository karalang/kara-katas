"""LeetCode 306 - Additive Number.

Mirror of additive_number.kara: the same search over the first two numbers'
lengths, with each number held as its decimal DIGITS and added by hand, so the
arithmetic is exact at any length. Python's ints would not overflow, but the
digit-list addition is kept to match the Kara arm algorithm-for-algorithm.
"""


def add_digits(a, b):
    rev = []
    i, j, carry = len(a) - 1, len(b) - 1, 0
    while i >= 0 or j >= 0 or carry > 0:
        s = carry
        if i >= 0:
            s += a[i]; i -= 1
        if j >= 0:
            s += b[j]; j -= 1
        rev.append(s % 10)
        carry = s // 10
    return rev[::-1]


def matches_at(d, pos, num):
    if pos + len(num) > len(d):
        return False
    return d[pos:pos + len(num)] == num


def no_leading_zero(d, lo, hi):
    return hi - lo == 1 or d[lo] != 0


def is_additive(s):
    d = [ord(ch) - 48 for ch in s]
    n = len(d)
    if n < 3:
        return False
    for len1 in range(1, n - 1):
        if not no_leading_zero(d, 0, len1):
            break
        for len2 in range(1, n - len1):
            if not no_leading_zero(d, len1, len1 + len2):
                break
            a = d[0:len1]
            b = d[len1:len1 + len2]
            pos, ok, steps = len1 + len2, True, 0
            while pos < n and ok:
                c = add_digits(a, b)
                if matches_at(d, pos, c):
                    pos += len(c)
                    a, b = b, c
                    steps += 1
                else:
                    ok = False
            if ok and pos == n and steps > 0:
                return True
    return False


def report(s):
    print('"%s" -> %s' % (s, "true" if is_additive(s) else "false"))


def main():
    report("112358")
    report("199100199")
    report("1023")
    report("000")
    report("011")
    report("123")
    report("122")
    report("")
    report("1")
    report("12")
    report("1023456")
    report("0235")
    report("0000")
    report("00000")
    report("199100")
    report("11235813213455891442333776109871597258441816765109461771128657")
    report("999999999999999999991100000000000000000000")
    report("12345678910111213141516171819202122")


if __name__ == "__main__":
    main()
