# LeetCode #942: DI String Match -- the smallest and largest left.
# Mirrors di_string_match.kara (the ★ arm) and prints the same output.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_letters(n):
    return "".join("I" if next_random() % 2 == 0 else "D" for _ in range(n))


def fits(s, perm):
    n = len(s)
    if len(perm) != n + 1:
        return False
    seen = [False] * (n + 1)
    for v in perm:
        if v < 0 or v > n or seen[v]:
            return False
        seen[v] = True
    for i in range(n):
        if (s[i] == "I") != (perm[i] < perm[i + 1]):
            return False
    return True


def verdict(s):
    return f"a permutation of 0 to {len(s)} that fits" if fits(s, di_string_match(s)) else "WRONG"


def main():
    global seed
    for s in ["IDID", "III", "DDI", "I", "D", "DIDI", "IIDD", "DDDIII"]:
        print(f'"{s}": {verdict(s)}')
    seed = 942
    letters = good = 0
    for _ in range(300):
        n = 1 + next_random() % 100
        s = random_letters(n)
        if fits(s, di_string_match(s)):
            good += 1
        letters += n
    print(f"300 random strings of {letters} letters: {good} answers fit")
    print(f"100000 I: {verdict('I' * 100000)}")
    print(f"100000 D: {verdict('D' * 100000)}")
    print(f"ID 50000 times: {verdict('ID' * 50000)}")
    print(f"100000 random letters: {verdict(random_letters(100000))}")


main()
