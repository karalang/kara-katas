# LeetCode #592: Fraction Addition and Subtraction -- a running sum.
#
# Mirrors fraction_addition.kara: one fraction at a time, added to a
# running fraction over the least common multiple of the denominators
# and reduced by the greatest common divisor as it goes.


def gcd(a, b):
    # Kara's `%` truncates toward zero, as C does; Python's floors, so
    # the remainder is taken with the sign of the dividend.
    if b == 0:
        return abs(a)
    r = abs(a) % abs(b)
    if a < 0:
        r = -r
    return gcd(b, r)


def digits(e, i):
    value = 0
    j = i
    while j < len(e) and e[j].isdigit():
        value = value * 10 + (ord(e[j]) - ord('0'))
        j += 1
    return value, j


def tdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def fraction_addition(expression):
    e = expression
    num, den, i = 0, 1, 0
    while i < len(e):
        sign = 1
        if e[i] == '-' or e[i] == '+':
            if e[i] == '-':
                sign = -1
            i += 1
        a, after_a = digits(e, i)
        b, after_b = digits(e, after_a + 1)
        i = after_b
        common = tdiv(den, gcd(den, b)) * b
        num = num * tdiv(common, den) + sign * a * tdiv(common, b)
        den = common
        g = gcd(num, den)
        num = tdiv(num, g)
        den = tdiv(den, g)
    return f"{num}/{den}"


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def coprime(a, b):
    x, y = a, b
    while y != 0:
        x, y = y, x % y
    return x == 1


def expression(count, seed):
    out = []
    for k in range(count):
        a = 1 + step(seed) % 10
        b = 1 + step(seed) % 10
        while not coprime(a, b):
            a = 1 + step(seed) % 10
            b = 1 + step(seed) % 10
        if step(seed) % 2 == 0:
            out.append('-')
        elif k > 0:
            out.append('+')
        out.append(f"{a}/{b}")
    return ''.join(out)


def show(e):
    print(f"{e} = {fraction_addition(e)}")


def main():
    show("-1/2+1/2")
    show("-1/2+1/2+1/3")
    show("1/3-1/2")
    show("3/7")
    show("-10/1")
    show("2/1+3/1-1/1")
    show("10/1+10/1+10/1+10/1+10/1+10/1+10/1+10/1+10/1+10/1")
    show("-10/1-10/1-10/1-10/1-10/1-10/1-10/1-10/1-10/1-10/1")
    show("1/1+1/2+1/3+1/4+1/5+1/6+1/7+1/8+1/9+1/10")
    show("1/1-1/2+1/3-1/4+1/5-1/6+1/7-1/8+1/9-1/10")
    show("1/6+1/3")
    show("1/10-1/10")
    seed = [592]
    zero = whole = checksum = 0
    for _ in range(1000):
        e = expression(1 + step(seed) % 10, seed)
        got = fraction_addition(e)
        if got.startswith("0/"):
            zero += 1
        if got.endswith("/1"):
            whole += 1
        for c in got:
            checksum = (checksum * 31 + ord(c)) % 1000000007
    print(f"1000 random expressions: {zero} zero, {whole} whole, checksum {checksum}")


main()
