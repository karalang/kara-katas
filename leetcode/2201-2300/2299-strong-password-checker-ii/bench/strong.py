# LeetCode #2299: Strong Password Checker II -- the bench, the ★ arm in
# Python. One pass over the letters: four flags set by the letter's kind,
# and the letter before, which must differ from each one.

seed = 2299


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    kinds = [
        "abcdefghijklmnopqrstuvwxyz",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "0123456789",
        "!@#$%^&*()-+",
    ]
    passwords = []
    for _ in range(200000):
        n = next_random() % 13 + 8
        width = next_random() % 12 + 1
        s = []
        for _ in range(n):
            kind = kinds[next_random() % 4]
            s.append(kind[next_random() % min(width, len(kind))])
        passwords.append("".join(s))
    count = len(passwords)
    check = 0
    for p in range(20):
        for i in range(count):
            w = passwords[(i + 7 * p) % count]
            check = (check * 31 + (len(w) if strong_password_checker_ii(w) else 1)) % 1000000007
    print(f"20 passes over 2 * 10^5 passwords: checksum {check}")


main()
