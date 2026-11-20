# LeetCode #1249 bench, in Python: the ★ arm (a stack of the places of
# the ( not yet closed, and a list of the characters to keep) on 50 random
# strings of 100000 characters built once, each with its own share of
# parentheses, each asked 4 times; every kept string folded into a
# checksum.


def min_remove_to_make_valid(s):
    keep = [True] * len(s)
    open_at = []
    for i, c in enumerate(s):
        if c == "(":
            open_at.append(i)
        elif c == ")":
            if open_at:
                open_at.pop()
            else:
                keep[i] = False
    for i in open_at:
        keep[i] = False
    return "".join(c for i, c in enumerate(s) if keep[i])


seed = 1249


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, percent):
    out = []
    for _ in range(n):
        if next_random() % 100 < percent:
            out.append("(" if next_random() % 2 == 0 else ")")
        else:
            out.append("abcde"[next_random() % 5])
    return "".join(out)


def main():
    texts = [random_text(100000, next_random() % 101) for _ in range(50)]
    check = 0
    for _ in range(4):
        for s in texts:
            kept = min_remove_to_make_valid(s)
            for c in kept:
                check = (check * 131 + ord(c)) % 1000000007
    print(f"4 rounds of 50 strings of 100000 characters: checksum {check}")


main()
