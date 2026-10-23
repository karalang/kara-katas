# LeetCode #903: Valid Permutations for DI Sequence -- Python mirror of the
# ranks-with-running-sums solution in num_perms_di_sequence.kara, with the
# same test harness.
#
# Let ways[j] count the orders of the first i + 1 numbers that fit the
# first i letters and end on the j-th smallest. After an 'I' the new
# number takes rank j when the old last ranked below j; after a 'D' when
# it ranked j or above. A running sum over the old row gives each in
# O(1). O(n^2).


def num_perms_di_sequence(s):
    m = 1000000007
    n = len(s)
    ways = [1]
    for i in range(1, n + 1):
        below = [0] * (i + 1)
        for k in range(i):
            below[k + 1] = (below[k] + ways[k]) % m
        nxt = [0] * (i + 1)
        for j in range(i + 1):
            if s[i - 1] == "I":
                nxt[j] = below[j]
            else:
                nxt[j] = (below[i] - below[j] + m) % m
        ways = nxt
    total = 0
    for w in ways:
        total = (total + w) % m
    return total


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f"s = \"{s}\" -> {num_perms_di_sequence(s)}")


# `len` letters: random, each 'D' with chance `d` in 10
def random_letters(length, d):
    return "".join("D" if next_random() % 10 < d else "I" for _ in range(length))


def main():
    global seed
    show("DID")
    show("D")
    show("I")
    show("III")
    show("DDD")
    show("ID")
    show("DI")
    show("IDID")
    show("DDIDI")
    show("IIDDII")
    # random cases of up to 200 letters, 'D' from 0 to 10 in 10
    seed = 903
    check = 0
    letters = 0
    for c in range(120):
        length = 1 + next_random() % 200
        got = num_perms_di_sequence(random_letters(length, c % 11))
        check = (check * 1000003 + got) % 1000000007
        letters += length
    print(f"120 cases ({letters} letters): checksum {check}")
    # LeetCode's largest: 200 random letters, and 200 alternating
    print(f"200 random letters -> {num_perms_di_sequence(random_letters(200, 5))}")
    zigzag = "".join("D" if i % 2 == 0 else "I" for i in range(200))
    print(f"200 letters DIDI... -> {num_perms_di_sequence(zigzag)}")


main()
