# LeetCode #678: Valid Parenthesis String -- the range of open counts.
# Mirrors the ★ arm (valid_parenthesis_string.kara) and its test harness.


def check_valid_string(s):
    low = 0
    high = 0
    for c in s:
        if c == '(':
            low += 1
            high += 1
        elif c == ')':
            low -= 1
            high -= 1
        else:
            low -= 1
            high += 1
        if high < 0:
            return False
        if low < 0:
            low = 0
    return low == 0


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def b(x):
    return "true" if x else "false"


def show(s):
    print(f'"{s}" -> {b(check_valid_string(s))}')


def nth_string(i, n):
    s = []
    p = 3 ** (n - 1)
    for _ in range(n):
        s.append("()*"[i // p % 3])
        p //= 3
    return "".join(s)


def random_string(rng, c):
    s = []
    if c % 3 == 0:
        n = 1 + rng.next() % 100
        for _ in range(n):
            s.append("()*"[rng.next() % 3])
        return "".join(s)
    half = 1 + rng.next() % 50
    opened = 0
    left = half
    while left > 0 or opened > 0:
        if left > 0 and (opened == 0 or rng.next() % 2 == 0):
            s.append('(')
            opened += 1
            left -= 1
        else:
            s.append(')')
            opened -= 1
    stars = rng.next() % 4
    changes = rng.next() % 3
    out = []
    for ch in s:
        r = rng.next() % 10
        if r < stars:
            out.append('*')
        elif r == 9 and rng.next() % 3 < changes:
            out.append(')' if ch == '(' else '(')
        else:
            out.append(ch)
    return "".join(out)


def main():
    for s in ["()", "(*)", "(*))", "(", ")", "*", "*)", "(*", ")*", "*(",
              "(*)(", "**((", "((**", "(*()", "())*(", "(((*)",
              "((*)(*))((*"]:
        show(s)
    print(f"50 ( then 50 * -> {b(check_valid_string('(' * 50 + '*' * 50))}")
    print(f"51 ( then 49 * -> {b(check_valid_string('(' * 51 + '*' * 49))}")
    print(f"(*)( 25 times -> {b(check_valid_string('(*)(' * 25))}")
    print(f"*) 50 times -> {b(check_valid_string('*)' * 50))}")
    print(f")* 50 times -> {b(check_valid_string(')*' * 50))}")
    counts = []
    for n in range(1, 9):
        counts.append(str(sum(1 for i in range(3 ** n)
                              if check_valid_string(nth_string(i, n)))))
    print(f"valid of 3^n, n = 1..8: {' '.join(counts)}")
    rng = Rng(678)
    total = 0
    valid = 0
    for c in range(1000):
        s = random_string(rng, c)
        n = len(s)
        if check_valid_string(s):
            valid += 1
            total = (total * 31 + n) % 1000000007
        else:
            total = (total * 31 + 1000 + n) % 1000000007
    print(f"1000 random strings: {valid} valid, checksum {total}")


main()
