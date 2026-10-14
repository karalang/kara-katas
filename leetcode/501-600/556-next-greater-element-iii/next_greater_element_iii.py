# LeetCode #556: Next Greater Element III -- Python mirror of the ★ arm
# (the next permutation of the digits); see next_greater_element_iii.kara.


def next_greater_element(n):
    d = []
    x = n
    while x > 0:
        d.append(x % 10)
        x //= 10
    d.reverse()
    i = len(d) - 2
    while i >= 0 and d[i] >= d[i + 1]:
        i -= 1
    if i < 0:
        return -1
    j = len(d) - 1
    while d[j] <= d[i]:
        j -= 1
    d[i], d[j] = d[j], d[i]
    d[i + 1:] = reversed(d[i + 1:])
    out = 0
    for v in d:
        out = out * 10 + v
    return -1 if out > 2147483647 else out


# ---- test harness ---------------------------------------------------------

seed = 556


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for n in [12, 21, 1, 11, 230241, 12443322, 1999999999, 2147483476, 2147483486, 2147483647, 1234567890, 9876543210 // 10]:
        print(f"{n} -> {next_greater_element(n)}")
    found = 0
    h = 0
    for t in range(300):
        top = 1000 if t % 3 == 0 else 10000000 if t % 3 == 1 else 2147483647
        a = next_random()
        b = next_random()
        n = 1 + (a * 65536 + b) % top
        got = next_greater_element(n)
        if got > 0:
            found += 1
        h = (h * 31 + got + 1) % 1000000007
    print(f"300 random numbers: {found} have a next, checksum {h}")


main()
