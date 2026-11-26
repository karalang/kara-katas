# LeetCode #1432: Max Difference You Can Get From Changing an Integer -- the
# Python mirror of max_diff.kara: the first digit that is not a 9 made one
# everywhere for the largest, and the first digit made a 1, or the first
# later digit that is neither a 0 nor a 1 made a 0, for the smallest


def max_diff(num):
    s = str(num)
    c = next((c for c in s if c != '9'), None)
    high = s.replace(c, '9') if c is not None else s
    first = s[0]
    if first != '1':
        low = s.replace(first, '1')
    else:
        c = next((c for c in s[1:] if c != '0' and c != '1'), None)
        low = s.replace(c, '0') if c is not None else s
    return int(high) - int(low)


# ---- test harness ---------------------------------------------------------

seed = 1432


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(" ".join(str(max_diff(n)) for n in [555, 9, 123456, 10000, 9288, 1, 100000000, 111]))
    total_all = sum(max_diff(n) for n in range(1, 100001))
    print(f"10^8: {max_diff(100000000)} {max_diff(99999999)} {max_diff(12345678)}, 1 to 10^5: {total_all}")
    check = 0
    total = 0
    for _ in range(2000):
        digits = 1 + next_random() % 8
        kind = next_random() % 3
        n = 0
        for d in range(digits):
            if kind == 0:
                digit = next_random() % 3
            elif kind == 1:
                digit = next_random() % 10
            else:
                digit = [1, 9][next_random() % 2]
            n = n * 10 + (1 if d == 0 and digit == 0 else digit)
        got = max_diff(n)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random numbers: {total} in all, checksum {check}")


main()
