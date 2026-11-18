# LeetCode #2301: Match Substring After Replacement -- the bench, the ★
# arm in Python. A table of which letter may stand for which, then every
# start of `sub` in `s` checked against it.

seed = 2301


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def match_replacement(s, sub, mappings):
    can = [False] * (128 * 128)
    for c in range(128):
        can[c * 128 + c] = True
    for old, new in mappings:
        can[ord(old) * 128 + ord(new)] = True
    s = s.encode()
    sub = sub.encode()
    k = len(sub)
    for start in range(len(s) - k + 1):
        ok = True
        for j in range(k):
            if not can[sub[j] * 128 + s[start + j]]:
                ok = False
                break
        if ok:
            return True
    return False


def main():
    texts, subs, maps = [], [], []
    for _ in range(50):
        s = "".join("ab"[next_random() % 2] for _ in range(20000))
        sub = []
        for _ in range(40):
            r = next_random() % 4
            sub.append("c" if r < 2 else "ab"[r - 2])
        mappings = [("c", "a"), ("c", "b")]
        for _ in range(998):
            old = "xyz"[next_random() % 3]
            new = "ab"[next_random() % 2]
            mappings.append((old, new))
        texts.append(s)
        subs.append("".join(sub))
        maps.append(mappings)
    check = 0
    for p in range(20):
        for c in range(50):
            ok = match_replacement(texts[(c + p) % 50], subs[c], maps[c])
            check = (check * 31 + (c + 1 if ok else 0)) % 1000000007
    print(f"20 passes over 50 cases of 20000 letters: checksum {check}")


main()
