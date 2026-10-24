# Benchmark: LeetCode #942 DI String Match -- the ★ arm, the smallest
# and largest left, on 20 strings of 100000 letters, LeetCode's longest,
# in 50 rounds. Mirrors di_string_match.kara, .c, .rs and go-seq/.


def di_string_match(s):
    lo, hi = 0, len(s)
    perm = []
    for c in s:
        if c == "I":
            perm.append(lo)
            lo += 1
        else:
            perm.append(hi)
            hi -= 1
    perm.append(lo)
    return perm


seed = 942


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 50
    count = 20
    n = 100000
    strings = []
    for _ in range(count):
        odds = 1 + next_random() % 15
        strings.append("".join("I" if next_random() % 16 < odds else "D" for _ in range(n)))
    check = 0
    for r in range(rounds):
        for i in range(count):
            perm = di_string_match(strings[(r + i) % count])
            check = (check * 1000003 + perm[0] * 3 + perm[n // 2] * 5 + perm[n] * 7) % 1000000007
    print(f"{rounds} rounds over {count} strings of {n} letters: checksum {check}")


main()
