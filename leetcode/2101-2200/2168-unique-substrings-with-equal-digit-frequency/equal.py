# LeetCode #2168: Unique Substrings With Equal Digit Frequency -- the
# Python mirror of equal.kara: each substring grown from its start with a
# count of each digit, kept in a set when the most times the digits is
# its length.


def equal_digit_frequency(s):
    n = len(s)
    found = set()
    for i in range(n):
        counts = [0] * 10
        kinds = 0
        most = 0
        for j in range(i, n):
            d = ord(s[j]) - ord("0")
            if counts[d] == 0:
                kinds += 1
            counts[d] += 1
            most = max(most, counts[d])
            if most * kinds == j - i + 1:
                found.add(s[i:j + 1])
    return len(found)


# ---- test harness ---------------------------------------------------------

seed = 2168


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f'"{s}" -> {equal_digit_frequency(s)}')


def digits(length, top):
    return "".join(str(next_random() % top) for _ in range(length))


def main():
    show("1212")
    show("12321")
    show("7")
    show("44444")
    show("0123456789")
    show("909090")
    total = 0
    check = 0
    for rnd in range(2000):
        length = next_random() % 20 + 1
        s = digits(length, [2, 3, 10][rnd % 3])
        u = equal_digit_frequency(s)
        total += u
        check = (check * 31 + u) % 1000000007
    print(f"2000 strings: {total} in all, checksum {check}")
    wide = digits(1000, 10)
    narrow = digits(1000, 2)
    cycle = "0123456789" * 100
    print(f"1000 digits: {equal_digit_frequency(wide)} {equal_digit_frequency(narrow)} {equal_digit_frequency(cycle)}")


main()
