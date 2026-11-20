# LeetCode #1271: Hexspeak -- Python mirror of the ★ arm (the hexadecimal
# digits taken from the lowest, 0 and 1 spelled O and I, 10 to 15 A to F,
# any other an error), with the same harness.


def to_hexspeak(num):
    n = int(num)
    letters = []
    while n > 0:
        d = n % 16
        if d == 0:
            letters.append("O")
        elif d == 1:
            letters.append("I")
        elif d >= 10:
            letters.append(chr(ord("A") + d - 10))
        else:
            return "ERROR"
        n //= 16
    return "".join(reversed(letters))


seed = 1271


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def spelled(length, digits):
    n = 0
    for i in range(length):
        d = digits[next_random() % len(digits)]
        while i == 0 and d == 0:
            d = digits[next_random() % len(digits)]
        n = n * 16 + d
    return n


def fold(check, s):
    c = (check * 131 + len(s)) % 1000000007
    for b in s.encode():
        c = (c * 131 + b) % 1000000007
    return c


print(f"{to_hexspeak('257')} {to_hexspeak('3')} {to_hexspeak('1')} {to_hexspeak('1000000000000')} {to_hexspeak('747823223228')}")
valid = 0
check = 0
letters = [0, 1, 10, 11, 12, 13, 14, 15]
for case in range(3000):
    if case % 3 == 0:
        a = next_random()
        b = next_random()
        n = (a * 32768 + b) % 1000000000000 + 1
    elif case % 3 == 1:
        n = spelled(next_random() % 10 + 1, letters)
    else:
        digits = letters + [next_random() % 8 + 2]
        n = spelled(next_random() % 10 + 1, digits)
    got = to_hexspeak(str(n))
    if got != "ERROR":
        valid += 1
    check = fold(check, got)
print(f"3000 random numbers: {valid} valid, checksum {check}")
