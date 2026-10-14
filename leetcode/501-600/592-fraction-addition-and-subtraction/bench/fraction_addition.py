# Benchmark for #592: Python mirror of the ★ arm (a running sum, reduced
# as it goes); see fraction_addition.kara. Kara's `/` and `%` truncate
# toward zero, as C does, so both are spelled out here.


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


# ---- benchmark ---------------------------------------------------------------

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


def main():
    count = 1000
    rounds = 1000
    seed = [592]
    expressions = [expression(10, seed) for _ in range(count)]
    negative = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            got = fraction_addition(expressions[(rnd * 7 + g) % count])
            if got.startswith("-"):
                negative += 1
            for c in got:
                checksum = (checksum * 31 + ord(c)) % 1000000007
    print(f"{count} expressions, {rounds} rounds: {negative} negative, checksum {checksum}")


main()
