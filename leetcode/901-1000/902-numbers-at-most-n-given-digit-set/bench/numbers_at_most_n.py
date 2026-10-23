# LeetCode #902: Numbers At Most N Given Digit Set -- bench program, Python.
#
# Lengths, then the digits of n from the left, asked about every one of
# the 511 sets of the digits 1 to 9, built once, in turn, each time with a
# random n from 1 to 10^9, and the counts folded into a checksum.


def at_most_n_given_digit_set(digits, n):
    s = str(n)
    k = len(s)
    d = len(digits)
    count = 0
    power = 1
    for _ in range(1, k):
        power *= d
        count += power
    for i in range(k):
        rest = k - i - 1
        ways = 1
        for _ in range(rest):
            ways *= d
        smaller = 0
        equal = False
        for digit in digits:
            c = digit[0]
            if c < s[i]:
                smaller += 1
            elif c == s[i]:
                equal = True
        count += smaller * ways
        if not equal:
            return count
    return count + 1


seed = 902


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    queries = 8000000
    sets = []
    for mask in range(1, 512):
        sets.append([str(c) for c in range(1, 10) if (mask >> (c - 1)) & 1 == 1])
    check = 0
    total = 0
    for q in range(queries):
        hi = next_random()
        lo = next_random()
        n = 1 + (hi * 32768 + lo) % 1000000000
        got = at_most_n_given_digit_set(sets[q % 511], n)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"{queries} queries over the 511 digit sets: counts summing to {total}, checksum {check}")


main()
