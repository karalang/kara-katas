# LeetCode #903: Valid Permutations for DI Sequence -- bench program, Python.
#
# Ranks of the last number with running sums, over one string of 4,000
# random letters built once. Each round counts its valid permutations,
# folds the count into a checksum and flips one letter.


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


seed = 903


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    length = 4000
    rounds = 12
    letters = ["D" if next_random() % 2 == 0 else "I" for _ in range(length)]
    check = 0
    for r in range(rounds):
        got = num_perms_di_sequence("".join(letters))
        check = (check * 31 + got) % 1000000007
        at = r * 7919 % length
        letters[at] = "I" if letters[at] == "D" else "D"
    print(f"{rounds} rounds over {length} letters: checksum {check}")


main()
