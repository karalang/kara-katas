# LeetCode #709: To Lower Case -- character by character.
#
# A mirror of to_lower_case.kara (the ★ arm) and its harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def to_lower_case(s):
    out = []
    for c in s:
        if "A" <= c <= "Z":
            out.append(chr(ord(c) + 32))
        else:
            out.append(c)
    return "".join(out)


def show(s):
    print(f'"{s}" -> "{to_lower_case(s)}"')


def random_string(n):
    return "".join(chr(32 + next_random() % 95) for _ in range(n))


def checksum(s):
    total = 0
    for b in s.encode():
        total = (total * 131 + b) % 1000000007
    return total


def main():
    global seed
    show("Hello")
    show("here")
    show("LOVELY")
    show("Q")
    show("@AZ[`az{")
    show("".join(chr(b) for b in range(32, 127)))
    seed = 709
    show(random_string(100))
    total = 0
    changed = 0
    for _ in range(1000):
        n = 1 + next_random() % 100
        s = random_string(n)
        t = to_lower_case(s)
        if t != s:
            changed += 1
        total = (total * 31 + checksum(t)) % 1000000007
    print(f"1000 random strings: {changed} changed, checksum {total}")


main()
