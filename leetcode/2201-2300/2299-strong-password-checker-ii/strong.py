# LeetCode #2299: Strong Password Checker II -- mirror of the ★ arm
# (strong.kara): one pass, four flags set by the letter's kind, and the
# letter before, which must differ from each one.


def strong_password_checker_ii(password):
    if len(password) < 8:
        return False
    lower = upper = digit = special = False
    prev = " "
    for c in password:
        if c == prev:
            return False
        if "a" <= c <= "z":
            lower = True
        elif "A" <= c <= "Z":
            upper = True
        elif "0" <= c <= "9":
            digit = True
        elif c in "!@#$%^&*()-+":
            special = True
        prev = c
    return lower and upper and digit and special


# ---- test harness ----------------------------------------------------------

seed = 2299


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


KINDS = [
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123456789",
    "!@#$%^&*()-+",
]


def random_password(n, start, width):
    s = []
    for _ in range(n):
        kind = KINDS[next_random() % 4]
        s.append(kind[(start + next_random() % min(width, len(kind))) % len(kind)])
    return "".join(s)


def main():
    cases = [
        "IloveLe3tcode!", "Me+You--IsMyDream", "1aB!",
        "aA1!aA1!", "aA1!aA1", "aA1!aA1!!",
        "AB1!AB1!", "ab1!ab1!", "aBc!aBc!", "aB1caB1c",
        "a", "aA1!" * 25,
    ]
    for p in cases:
        print(f"{len(p)} {'true' if strong_password_checker_ii(p) else 'false'}")
    strong = 0
    check = 0
    for _ in range(20000):
        n = next_random() % 16 + 1
        width = next_random() % 12 + 1
        start = next_random() % 26
        p = random_password(n, start, width)
        ok = strong_password_checker_ii(p)
        if ok:
            strong += 1
        check = (check * 31 + (n if ok else 100 + n)) % 1000000007
    print(f"20000 passwords: {strong} strong, checksum {check}")


main()
