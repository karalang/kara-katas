# LeetCode #1417, Python mirror of reformat.kara: the letters and the
# digits apart, each in its order, woven together from the larger group,
# the letters first on a tie.


def reformat(s):
    letters = [c for c in s if c.islower()]
    digits = [c for c in s if c.isdigit()]
    if abs(len(letters) - len(digits)) > 1:
        return ""
    first, second = (digits, letters) if len(digits) > len(letters) else (letters, digits)
    out = []
    for i in range(len(first)):
        out.append(first[i])
        if i < len(second):
            out.append(second[i])
    return "".join(out)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, digits):
    out = []
    for _ in range(n):
        r = next_random()
        if r % digits == 0:
            out.append(str(r // 7 % 10))
        else:
            out.append("abcxyz"[r // 7 % 6])
    return "".join(out)


def shown(s):
    return s if s else "-"


def main():
    global seed
    print(" ".join(shown(reformat(s)) for s in ["a0b1c2", "leetcode", "1229857369", "covid2019", "a", "7", "ab12c"]))
    seed = 1417
    even = drawn(500, 2)
    half = "".join(f"{i % 10}q" for i in range(250))
    print(f"500 characters: {len(reformat(even))} {reformat(half)[:20]} {len(reformat(half[1:]))}")
    check = 0
    empty = 0
    for _ in range(2000):
        n = 1 + next_random() % 30
        out = reformat(drawn(n, 2 + next_random() % 2))
        if not out:
            empty += 1
        for b in out.encode():
            check = (check * 131 + b) % 1000000007
        check = (check * 131 + 7) % 1000000007
    print(f"2000 random strings: {empty} empty, checksum {check}")


main()
