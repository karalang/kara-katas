# LeetCode #482: License Key Formatting -- mirror of
# license_key_formatting.kara (the ★ arm).


def license_key_formatting(s, k):
    backwards = []
    in_group = 0
    for c in reversed(s):
        if c == "-":
            continue
        if in_group == k:
            backwards.append("-")
            in_group = 0
        backwards.append(c.upper())
        in_group += 1
    backwards.reverse()
    return "".join(backwards)


def show(s, k):
    print(f"'{s}', k = {k} -> '{license_key_formatting(s, k)}'")


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    show("5F3Z-2e-9-w", 4)
    show("2-5g-3-J", 2)
    show("---", 3)
    show("a", 1)
    show("abcdef", 10)
    show("a-b-c-d", 1)
    show("--a--bc--", 2)
    show("r5z-9kx-m", 3)
    show("AA-aa-AA", 2)
    alphabet = list("abcxyzABCXYZ0189")
    count = 300
    seed = [482]
    length = 0
    dashes = 0
    checksum = 0
    for _ in range(count):
        s = []
        size = 1 + next_random(seed) % 40
        for _ in range(size):
            if next_random(seed) % 4 == 0:
                s.append("-")
            else:
                s.append(alphabet[next_random(seed) % len(alphabet)])
        k = 1 + next_random(seed) % 8
        key = license_key_formatting("".join(s), k)
        for c in key:
            length += 1
            if c == "-":
                dashes += 1
            checksum = (checksum * 31 + ord(c)) % 1000000007
        checksum = (checksum * 31 + 7) % 1000000007
    print(f"{count} random cases: {length} characters, {dashes} dashes, checksum {checksum}")


main()
