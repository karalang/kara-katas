# LeetCode #1556: Thousand Separator -- bench: the ★ arm (a dot before
# every digit whose distance from the end is a positive multiple of three)
# over 1000000 numbers below 2^31, each with its own count of 1 to 10
# digits, drawn once, each asked 3 times. Python mirror of separator.kara.


def thousand_separator(n):
    digits = str(n)
    length = len(digits)
    out = []
    for i, c in enumerate(digits):
        if i > 0 and (length - i) % 3 == 0:
            out.append(".")
        out.append(c)
    return "".join(out)


seed = 1556


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    numbers = []
    for _ in range(1000000):
        digits = next_random() % 10 + 1
        top = 10 ** digits
        wide = (next_random() * 32768 + next_random()) * 32768 + next_random()
        numbers.append(min(wide % top, 2147483647))
    check = 0
    length = 0
    for _ in range(3):
        for n in numbers:
            text = thousand_separator(n)
            length += len(text)
            for b in text.encode():
                check = (check * 31 + b + 1) % 1000000007
    print(f"3 passes over 1000000 numbers: {length} characters, checksum {check}")


main()
