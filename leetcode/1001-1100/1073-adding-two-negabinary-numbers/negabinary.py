# LeetCode #1073: Adding Two Negabinary Numbers -- the Python mirror of
# negabinary.kara (the ★ arm): the digits added from the low end with a
# carry of -1, 0 or 1, the leading zeros dropped.


def add_negabinary(a, b):
    i, j, carry = len(a) - 1, len(b) - 1, 0
    digits = []
    while i >= 0 or j >= 0 or carry != 0:
        s = carry
        if i >= 0:
            s += a[i]
            i -= 1
        if j >= 0:
            s += b[j]
            j -= 1
        digits.append(s & 1)
        carry = -(s >> 1)
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return digits[::-1]


seed = 1073


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_number(longest):
    n = next_random() % longest + 1
    if n == 1:
        return [next_random() % 2]
    return [1] + [next_random() % 2 for _ in range(n - 1)]


def show(digits):
    return "".join(str(d) for d in digits)


def checksum(digits):
    check = len(digits)
    for d in digits:
        check = (check * 31 + d + 1) % 1000000007
    return check


def main():
    examples = [
        ([1, 1, 1, 1, 1], [1, 0, 1]),
        ([0], [0]),
        ([0], [1]),
        ([1], [1]),
        ([1, 1], [1]),
        ([1, 1, 0], [1, 1, 0]),
        ([1, 0, 1, 0, 1], [1, 1, 1, 1]),
        ([1, 1, 1], [1, 1, 1, 1, 1, 1]),
        ([1, 0, 0, 0, 0, 0, 0, 1], [1, 1]),
    ]
    for a, b in examples:
        print(f"{show(a)} + {show(b)} -> {show(add_negabinary(a, b))}")
    for count, longest, label in [(3000, 12, "3000 pairs up to 12 digits"), (300, 1000, "300 pairs up to 1000 digits")]:
        zeros = digits = check = 0
        for _ in range(count):
            a = random_number(longest)
            b = random_number(longest)
            x = add_negabinary(a, b)
            if x == [0]:
                zeros += 1
            digits += len(x)
            check = (check * 31 + checksum(x)) % 1000000007
        print(f"{label}: {zeros} zero, {digits} digits, checksum {check}")
    ones = [1] * 1000
    alternating = [(k + 1) % 2 for k in range(1000)]
    print(f"1000 ones twice: {len(add_negabinary(ones, ones))} digits, checksum {checksum(add_negabinary(ones, ones))}")
    print(f"1000 ones and 1: {show(add_negabinary(ones, [1])[:8])}.. {len(add_negabinary(ones, [1]))} digits")
    print(f"1010.. and 999 ones: {len(add_negabinary(alternating, ones[1:]))} digits, checksum {checksum(add_negabinary(alternating, ones[1:]))}")
    print(f"1 and 1000 ones: {show(add_negabinary([1], ones)[:8])}.. {len(add_negabinary([1], ones))} digits")


main()
