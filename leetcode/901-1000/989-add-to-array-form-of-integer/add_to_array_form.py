# LeetCode #989: Add to Array-Form of Integer -- mirror of the ★ arm
# (add_to_array_form.kara), k carried in from the last digit.


def add_to_array_form(num, k):
    out = []
    carry = k
    i = len(num) - 1
    while i >= 0 or carry > 0:
        if i >= 0:
            carry += num[i]
            i -= 1
        out.append(carry % 10)
        carry //= 10
    out.reverse()
    return out


seed = 989


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_num(n, nines):
    # n digits, no leading zero unless the number is 0; a digit is 9
    # with chance nines in 8, otherwise any digit
    out = []
    for i in range(n):
        if next_random() % 8 < nines:
            d = 9
        else:
            d = next_random() % 10
        if i == 0 and n > 1 and d == 0:
            d = 1
        out.append(d)
    return out


def shown(ds):
    if len(ds) > 20:
        return f"{len(ds)} digits, starting {''.join(map(str, ds[:6]))}, ending {''.join(map(str, ds[-6:]))}"
    return "[" + ", ".join(map(str, ds)) + "]"


def main():
    cases = [
        ([1, 2, 0, 0], 34),
        ([2, 7, 4], 181),
        ([2, 1, 5], 806),
        ([0], 1),
        ([9, 9, 9], 1),
        ([0], 10000),
        ([5], 9995),
        ([1], 9999),
        ([9, 9, 9, 9, 9], 10000),
        ([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 1),
    ]
    for num, k in cases:
        print(f"{shown(num)} + {k} -> {shown(add_to_array_form(num, k))}")
    print(f"10000 nines + 1 -> {shown(add_to_array_form([9] * 10000, 1))}")
    print(f"10000 digits 1 to 0 + 10000 -> {shown(add_to_array_form([(i + 1) % 10 for i in range(10000)], 10000))}")
    for count, most, nines in [(300, 6, 2), (3000, 100, 4), (300, 30, 7), (3, 10000, 1)]:
        digits = 0
        out_digits = 0
        check = 0
        for _ in range(count):
            n = most if count == 3 else 1 + next_random() % most
            num = random_num(n, nines)
            k = 1 + next_random() % 10000
            got = add_to_array_form(num, k)
            digits += n
            out_digits += len(got)
            for d in got:
                check = (check * 31 + d + 1) % 1000000007
        print(f"{count} random sums of up to {most} digits: {digits} digits in, {out_digits} out, checksum {check}")


main()
