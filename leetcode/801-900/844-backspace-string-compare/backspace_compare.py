# LeetCode #844: Backspace String Compare -- Python mirror of the ★ arm and its harness.


def next_kept(s, i):
    skip = 0
    while i >= 0:
        if s[i] == "#":
            skip += 1
        elif skip > 0:
            skip -= 1
        else:
            return i
        i -= 1
    return -1


def backspace_compare(s, t):
    i = next_kept(s, len(s) - 1)
    j = next_kept(t, len(t) - 1)
    while i >= 0 and j >= 0:
        if s[i] != t[j]:
            return False
        i = next_kept(s, i - 1)
        j = next_kept(t, j - 1)
    return i < 0 and j < 0


def show(s, t):
    print(f'"{s}" vs "{t}" -> {"true" if backspace_compare(s, t) else "false"}')


seed = 844


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, k, hashes):
    out = []
    for _ in range(n):
        if next_random() % 10 < hashes:
            out.append("#")
        else:
            out.append(chr(97 + next_random() % k))
    return "".join(out)


def padded(s, k, extra):
    cs = list(s)
    for _ in range(extra):
        at = next_random() % (len(cs) + 1)
        cs.insert(at, "#")
        cs.insert(at, chr(97 + next_random() % k))
    if next_random() % 3 == 0:
        at = next_random() % len(cs)
        cs[at] = "#" if next_random() % 2 == 0 else chr(97 + next_random() % k)
    return "".join(cs)


def main():
    for s, t in [("ab#c", "ad#c"), ("ab##", "c#d#"), ("a#c", "b"), ("a", "a"), ("#", "##"),
                 ("###a", "a"), ("a##b", "#b"), ("abc", "ab"), ("ab", "abc##c"),
                 ("bxj##tw", "bxo#j##tw"), ("bxj##tw", "bxj###tw"), ("nzp#o#g", "b#nzp#o#g"),
                 ("y#fo##f", "y#f#o##f")]:
        show(s, t)
    long_s = "".join(chr(97 + i % 26) + "#" for i in range(100))
    long_t = "".join("#" + chr(97 + i % 26) for i in range(100))
    show(long_s[:20], long_t[:20])
    same = "true" if backspace_compare(long_s, long_t) else "false"
    print(f"200 characters, letters each undone vs each undone before: {same}")
    equal = 0
    check = 0
    for r in range(2000):
        n = 1 + next_random() % 30
        k = 1 + next_random() % 3
        hashes = next_random() % 6
        s = random_text(n, k, hashes)
        if r % 2 == 0:
            t = random_text(1 + next_random() % 30, k, hashes)
        else:
            t = padded(s, k, next_random() % 5)
        ok = backspace_compare(s, t)
        if ok:
            equal += 1
        check = (check * 31 + (r if ok else 1)) % 1000000007
    print(f"2000 random pairs: {equal} equal, checksum {check}")


main()
