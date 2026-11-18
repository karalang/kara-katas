# LeetCode #2301: Match Substring After Replacement -- mirror of the ★
# arm (match.kara): a table of which letter may stand for which, and
# every start of `sub` in `s` checked against it.


def match_replacement(s, sub, mappings):
    can = [False] * (128 * 128)
    for c in range(128):
        can[c * 128 + c] = True
    for old, new in mappings:
        can[ord(old) * 128 + ord(new)] = True
    for start in range(len(s) - len(sub) + 1):
        if all(can[ord(sub[j]) * 128 + ord(s[start + j])] for j in range(len(sub))):
            return True
    return False


# ---- test harness ----------------------------------------------------------

seed = 2301


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        ("fool3e7bar", "leet", [("e", "3"), ("t", "7"), ("t", "8")]),
        ("fooleetbar", "f00l", [("o", "0")]),
        ("Fool33tbaR", "leetd", [("e", "3"), ("t", "7"), ("t", "8"), ("d", "b"), ("p", "b")]),
        ("abc", "abc", []),
        ("abcabd", "abd", []),
        ("xcz", "xaz", [("a", "b"), ("b", "c")]),
        ("q9q", "q9q", [("q", "q")]),
    ]
    for s, sub, mappings in cases:
        print(f"{s} {sub}: {'true' if match_replacement(s, sub, mappings) else 'false'}")
    letters = "abcAB01"
    found = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 30 + 1
        k = next_random() % min(n, 8) + 1
        s = "".join(letters[next_random() % 7] for _ in range(n))
        sub = "".join(letters[next_random() % 7] for _ in range(k))
        mappings = []
        for _ in range(next_random() % 13):
            old = letters[next_random() % 7]
            new = letters[next_random() % 7]
            mappings.append((old, new))
        ok = match_replacement(s, sub, mappings)
        if ok:
            found += 1
        check = (check * 31 + (n * 100 + k if ok else 7)) % 1000000007
    print(f"2000 cases: {found} match, checksum {check}")


main()
