# LeetCode #1397: Find All Good Strings -- Python mirror of the ★ arm:
# the strings built a letter at a time, counted by how much of `evil`
# their end matches and whether they are still equal to s1's prefix and
# to s2's, the matches stepped through the Knuth-Morris-Pratt automaton.


def slot(j, low, high):
    return j * 4 + (2 if low else 0) + (1 if high else 0)


def find_good_strings(n, s1, s2, evil):
    modulus = 1000000007
    lo = s1.encode()
    hi = s2.encode()
    e = evil.encode()
    m = len(e)
    border = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and e[i] != e[k]:
            k = border[k - 1]
        if e[i] == e[k]:
            k += 1
        border[i] = k
    nxt = [0] * (m * 26)
    for j in range(m):
        for c in range(26):
            if e[j] == 97 + c:
                nxt[j * 26 + c] = j + 1
            elif j > 0:
                nxt[j * 26 + c] = nxt[border[j - 1] * 26 + c]
    ways = [0] * (m * 4)
    ways[slot(0, True, True)] = 1
    for i in range(n):
        after = [0] * (m * 4)
        for j in range(m):
            for low in (False, True):
                for high in (False, True):
                    w = ways[slot(j, low, high)]
                    if w == 0:
                        continue
                    first = lo[i] - 97 if low else 0
                    last = hi[i] - 97 if high else 25
                    for c in range(first, last + 1):
                        to = nxt[j * 26 + c]
                        if to == m:
                            continue
                        at = slot(to, low and c == first, high and c == last)
                        after[at] = (after[at] + w) % modulus
        ways = after
    total = 0
    for w in ways:
        total = (total + w) % modulus
    return total


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n letters drawn from the first `letters` of the alphabet
def drawn(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


# a case of the given sizes: two strings of n letters, the smaller first,
# and an evil string of m letters
def case_of(n, letters, m, evil_letters):
    a = drawn(n, letters)
    b = drawn(n, letters)
    evil = drawn(m, evil_letters)
    return (a, b, evil) if a <= b else (b, a, evil)


def main():
    global seed
    shown = [
        find_good_strings(2, "aa", "da", "b"),
        find_good_strings(8, "leetcode", "leetgoes", "leet"),
        find_good_strings(2, "gx", "gz", "x"),
        find_good_strings(3, "abc", "abc", "d"),
        find_good_strings(3, "abc", "abc", "bc"),
    ]
    print(" ".join(str(x) for x in shown))
    seed = 1397
    top = "z" * 500
    big = []
    for m in [1, 8, 50]:
        low = drawn(500, 3)
        evil = drawn(m, 2)
        big.append(str(find_good_strings(500, low, top, evil)))
    print(f"n = 500: {' '.join(big)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 12
        letters = 1 + next_random() % 26
        m = 1 + next_random() % 4
        evil_letters = 1 + next_random() % 3
        a, b, evil = case_of(n, letters, m, evil_letters)
        got = find_good_strings(n, a, b, evil)
        total = (total + got) % 1000000007
        check = (check * 131 + got) % 1000000007
    print(f"2000 random cases: {total} in all, checksum {check}")


main()
