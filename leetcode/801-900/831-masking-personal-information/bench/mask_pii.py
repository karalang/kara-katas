# Benchmark for #831: Masking Personal Information -- the ★ arm (by the rules).
#
# Mirrors mask_pii.kara: an email keeps its name's first and last letter,
# lowered, around five `*`, and its domain lowered; a phone number shows
# its last four digits and masks the country code, the digits before the
# last ten.


def mask_pii(s):
    at = s.find("@")
    if at >= 0:
        lower = s.lower()
        return f"{lower[0:1]}*****{lower[at - 1:]}"
    digits = ""
    for c in s:
        if c.isdigit():
            digits += c
    n = len(digits)
    local = f"***-***-{digits[n - 4:]}"
    if n == 10:
        return local
    return f"+{'*' * (n - 10)}-{local}"


def main():
    count, rounds = 64, 12000000
    separators = ['+', '-', '(', ')', ' ']
    seed = 831

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def letter():
        r = next_random() % 52
        return chr(97 + r) if r < 26 else chr(65 + r - 26)

    strings = []
    for g in range(count):
        s = ""
        if g % 2 == 0:
            for _ in range(2 + next_random() % 19):
                s += letter()
            s += "@"
            for _ in range(1 + next_random() % 8):
                s += letter()
            s += "."
            for _ in range(1 + next_random() % 8):
                s += letter()
        else:
            for _ in range(10 + next_random() % 4):
                if next_random() % 3 == 0:
                    s += separators[next_random() % 5]
                s += chr(48 + next_random() % 10)
        strings.append(s)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        m = mask_pii(strings[rnd % count])
        total += len(m)
        checksum = (checksum * 131 + ord(m[-1])) % 1000000007
    print(f"{rounds} rounds of {count} strings: {total} characters, checksum {checksum}")


main()
