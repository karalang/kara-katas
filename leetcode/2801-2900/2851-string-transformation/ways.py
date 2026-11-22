# LeetCode #2851: String Transformation -- the Python mirror of the ★
# arm: the shifts that turn s into t by the prefix function of t over
# s + s, and the closed form for the ways k nonzero shifts land on each.

MOD = 1000000007


def number_of_ways(s, t, k):
    n = len(s)
    text = s + s
    fail = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and t[i] != t[j]:
            j = fail[j - 1]
        if t[i] == t[j]:
            j += 1
        fail[i] = j
    at_zero = elsewhere = 0
    j = 0
    for i in range(2 * n - 1):
        while j > 0 and text[i] != t[j]:
            j = fail[j - 1]
        if text[i] == t[j]:
            j += 1
        if j == n:
            if i + 1 == n:
                at_zero += 1
            else:
                elsewhere += 1
            j = fail[j - 1]
    all_ = pow(n - 1, k, MOD)
    sign = 1 if k % 2 == 0 else MOD - 1
    inverse = pow(n, MOD - 2, MOD)
    zero_ways = (all_ + (n - 1) * sign) % MOD * inverse % MOD
    other_ways = (all_ - sign + MOD) % MOD * inverse % MOD
    return (at_zero * zero_ways + elsewhere * other_ways) % MOD


seed = 2851


def nr():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def rotated(s, r):
    n = len(s)
    return s[n - r:] + s[:n - r]


def main():
    print(number_of_ways("abcd", "cdab", 2), number_of_ways("ababab", "ababab", 1))
    print(number_of_ways("ab", "ab", 10**15), number_of_ways("ab", "ba", 10**15 + 1), number_of_ways("ab", "ba", 10**15))
    same = "a" * 2000
    print(number_of_ways(same, same, 10**15))
    check = matched = 0
    for c in range(3060):
        small = c < 3000
        n = nr() % 5 + 2 if small else nr() % 1999 + 2
        block = n if small else nr() % 8 + 1
        letters = 2 if small else nr() % 3 + 1
        unit = "".join(chr(97 + nr() % letters) for _ in range(block))
        s = "".join(unit[i % block] for i in range(n))
        if small:
            t = "".join(chr(97 + nr() % 2) for _ in range(n))
        elif nr() % 3 < 2:
            t = rotated(s, nr() % n)
        else:
            t = "".join(chr(97 + nr() % letters) for _ in range(n))
        if small:
            k = nr() % 20 + 1
        else:
            a = nr()
            k = (a * 30000 + nr()) * 1000 + 1
        ways = number_of_ways(s, t, k)
        if ways > 0:
            matched += 1
        check = (check * 31 + ways) % 1000000007
        if c == 2999:
            print(f"3000 short pairs: {matched} with a way, checksum {check}")
            matched = check = 0
    print(f"60 long pairs: {matched} with a way, checksum {check}")


main()
