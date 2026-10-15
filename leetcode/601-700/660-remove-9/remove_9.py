# LeetCode #660: Remove 9 -- base 9, read as base 10.
# Mirrors the ★ arm (remove_9.kara) and its test harness.


def new_integer(n):
    rest, place, out = n, 1, 0
    while rest > 0:
        out += rest % 9 * place
        rest //= 9
        place *= 10
    return out


# ---- test harness ---------------------------------------------------------


def has_nine(x):
    return "9" in str(x)


def main():
    print(f"n = 9 -> {new_integer(9)}")
    print(f"n = 10 -> {new_integer(10)}")
    for n in [1, 8, 80, 81, 728, 729, 6560, 6561, 800000000]:
        print(f"n = {n} -> {new_integer(n)}")
    x = 0
    agree = 0
    s = 0
    for n in range(1, 20001):
        x += 1
        while has_nine(x):
            x += 1
        got = new_integer(n)
        if got == x:
            agree += 1
        s = (s * 31 + got) % 1000000007
    print(f"n = 1 to 20000: {agree} agree with counting up, checksum {s}")
    s = 0
    n = 7
    for _ in range(1000):
        n = (n * 7919 + 104729) % 800000000 + 1
        s = (s * 31 + new_integer(n)) % 1000000007
    print(f"1000 spread values: checksum {s}")


main()
