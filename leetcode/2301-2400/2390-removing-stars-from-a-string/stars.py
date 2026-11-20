# LeetCode #2390: Removing Stars From a String -- a Python mirror of the
# ★ arm, a stack: a letter pushed, a star popping the letter closest to
# its left. Prints the same output as stars.kara.

seed = 0


def remove_stars(s):
    stack = []
    for c in s:
        if c == "*":
            if stack:
                stack.pop()
        else:
            stack.append(c)
    return "".join(stack)


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def starred(length, odds):
    out = []
    depth = 0
    for _ in range(length):
        if depth > 0 and next_random() % odds == 0:
            out.append("*")
            depth -= 1
        else:
            out.append(chr(ord("a") + next_random() % 26))
            depth += 1
    return "".join(out)


def letters_checksum(s):
    check = 0
    for c in s:
        check = (check * 31 + (ord(c) - ord("a") + 1)) % 1000000007
    return check


def main():
    global seed
    for s in ["leet**cod*e", "erase*****", "a*b", "abc**de***fg", "kara"]:
        print(f"[{remove_stars(s)}]")
    seed = 2390
    third = remove_stars(starred(100000, 3))
    half = remove_stars(starred(100000, 2))
    print(f"10^5 characters: {letters_checksum(third)} of {len(third)}, {letters_checksum(half)} of {len(half)}")
    check = 0
    total = 0
    empty = 0
    for _ in range(3000):
        length = 1 + next_random() % 30
        odds = 1 + next_random() % 4
        t = remove_stars(starred(length, odds))
        check = (check * 31 + letters_checksum(t)) % 1000000007
        total += len(t)
        if len(t) == 0:
            empty += 1
    print(f"3000 strings: checksum {check}, {total} letters left, {empty} empty")


if __name__ == "__main__":
    main()
