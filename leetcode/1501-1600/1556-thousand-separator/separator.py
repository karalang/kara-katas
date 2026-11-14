# LeetCode #1556: Thousand Separator -- the Python mirror of
# separator.kara, the ★ arm: a dot before each digit whose distance from
# the end is a positive multiple of three. Prints byte-identical output.


def thousand_separator(n):
    digits = str(n)
    length = len(digits)
    out = []
    for i, c in enumerate(digits):
        if i > 0 and (length - i) % 3 == 0:
            out.append(".")
        out.append(c)
    return "".join(out)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix_text(check, text):
    for b in text.encode():
        check = (check * 31 + b + 1) % 1000000007
    return (check * 31 + 7) % 1000000007


def batch(count):
    check = 0
    dots = 0
    for _ in range(count):
        digits = next_random() % 10 + 1
        top = 10 ** digits
        wide = (next_random() * 32768 + next_random()) * 32768 + next_random()
        n = min(wide % top, 2147483647)
        text = thousand_separator(n)
        dots += text.count(".")
        check = mix_text(check, text)
    print(f"{count} numbers: {dots} dots, checksum {check}")


def main():
    global seed
    for n in [987, 1234, 123456789, 0, 1000, 999999, 1000000, 100, 10000, 2147483647]:
        print(f'{n} -> "{thousand_separator(n)}"')
    seed = 1556
    batch(30000)


main()
