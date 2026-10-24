# Benchmark: LeetCode #972 Equal Rational Numbers -- the ★ arm, both as
# fractions in lowest terms, on 1000 random pairs of strings. Mirrors
# is_rational_equal.kara, .c, .rs and go-seq/.


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def fraction(s):
    whole, shift, rep, nines, part = 0, 1, 0, 0, 0
    for c in s:
        if c == ".":
            part = 1
        elif c == "(":
            part = 2
        elif c != ")":
            d = ord(c) - 48
            if part == 2:
                rep = rep * 10 + d
                nines = nines * 10 + 9
            else:
                whole = whole * 10 + d
                if part == 1:
                    shift *= 10
    if nines == 0:
        num, den = whole, shift
    else:
        num, den = whole * nines + rep, shift * nines
    g = gcd(num, den)
    return (num // g, den // g)


def is_rational_equal(s, t):
    return fraction(s) == fraction(t)


seed = 972


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digits(length):
    return "".join(str(next_random() % 10) for _ in range(length))


def text(x):
    int_, non, rep, dot = x
    s = str(int_)
    if dot or non or rep:
        s += "."
    s += non
    if rep:
        s += "(" + rep + ")"
    return s


def random_num():
    length = 1 + next_random() % 4
    int_ = next_random() % 10
    for _ in range(1, length):
        int_ = int_ * 10 + next_random() % 10
    non = digits(next_random() % 5)
    rep = "" if next_random() % 3 == 0 else digits(1 + next_random() % 4)
    return (int_, non, rep, next_random() % 2 == 0)


def variant(x):
    int_, non, rep, dot = x
    steps = 1 + next_random() % 3
    for _ in range(steps):
        kind = next_random() % 7
        r = len(rep)
        if kind == 0 and r > 0 and len(non) < 4:
            non += rep[0]
            rep = rep[1:] + rep[0]
        elif kind == 1 and r > 0 and 2 * r <= 4:
            rep = rep + rep
        elif kind == 2 and r == 0 and len(non) < 4:
            non += "0"
        elif kind == 3 and r == 0:
            rep = "0"
        elif kind == 4 and r == 0:
            if non and non[-1] != "0":
                non = non[:-1] + str(int(non[-1]) - 1)
                rep = "9"
            elif not non and int_ > 0:
                int_ -= 1
                rep = "9"
        elif kind == 5 and rep in ("0", "00", "000", "0000"):
            rep = ""
            dot = True
        elif kind == 6 and r % 2 == 0 and r > 0 and rep[: r // 2] == rep[r // 2 :]:
            rep = rep[: r // 2]
    return (int_, non, rep, dot)


def nudge(s):
    places = [i for i, c in enumerate(s) if c.isdigit()]
    at = places[next_random() % len(places)]
    old = int(s[at])
    new = next_random() % 9
    if new >= old:
        new += 1
    if at == 0 and new == 0 and len(s) > 1 and s[1].isdigit():
        new = 1 + old % 9
        if new == old:
            new = 9
    return s[:at] + str(new) + s[at + 1 :]


def random_pair(c):
    x = random_num()
    if c % 3 == 0:
        return (text(x), text(variant(x)))
    if c % 3 == 1:
        y = text(variant(x))
        return (text(x), nudge(y))
    return (text(x), text(random_num()))


def main():
    rounds, count = 1000, 1000
    pairs = [random_pair(c) for c in range(count)]
    equal = check = 0
    for r in range(rounds):
        for i in range(count):
            s, t = pairs[(r + i) % count]
            if is_rational_equal(s, t):
                equal += 1
                check = (check * 2 + 1) % 1000000007
            else:
                check = check * 2 % 1000000007
    print(f"{rounds} rounds over {count} pairs: {equal} equal, checksum {check}")


main()
