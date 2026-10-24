# LeetCode #943: Find the Shortest Superstring -- the most letters saved.
# Mirrors shortest_superstring.kara (the ★ arm) and its harness.


def overlap(a, b):
    k = min(len(a), len(b)) - 1
    while k > 0:
        if a[len(a) - k:] == b[:k]:
            return k
        k -= 1
    return 0


def shortest_superstring(words):
    n = len(words)
    ov = [0] * (n * n)
    for i in range(n):
        for j in range(n):
            if i != j:
                ov[i * n + j] = overlap(words[i], words[j])
    full = (1 << n) - 1
    saved = [-1] * ((full + 1) * n)
    before = [-1] * ((full + 1) * n)
    for mask in range(1, full + 1):
        for last in range(n):
            if (mask >> last) & 1 == 1:
                rest = mask ^ (1 << last)
                if rest == 0:
                    saved[mask * n + last] = 0
                else:
                    for p in range(n):
                        if (rest >> p) & 1 == 1:
                            s = saved[rest * n + p] + ov[p * n + last]
                            if s > saved[mask * n + last]:
                                saved[mask * n + last] = s
                                before[mask * n + last] = p
    last = 0
    for w in range(1, n):
        if saved[full * n + w] > saved[full * n + last]:
            last = w
    order = []
    mask = full
    while last >= 0:
        order.append(last)
        p = before[mask * n + last]
        mask = mask ^ (1 << last)
        last = p
    out = words[order[-1]]
    i = len(order) - 1
    while i > 0:
        a = order[i]
        b = order[i - 1]
        out = out + words[b][ov[a * n + b]:]
        i -= 1
    return out


seed = 943


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(next_random() % letters + 97) for _ in range(length))


def without_inside(words):
    kept = []
    for w in words:
        if all(not (w in k or k in w) for k in kept):
            kept.append(w)
    return kept


def verdict(words):
    s = shortest_superstring(words)
    for w in words:
        if w not in s:
            return "WRONG"
    return f"length {len(s)}, holding every word"


def main():
    examples = [
        ["alex", "loves", "leetcode"],
        ["catg", "ctaagt", "gcta", "ttca", "atgcatc"],
        ["word"],
        ["abc", "bcd", "cde"],
        ["cde", "abc", "bcd"],
        ["ab", "cd", "ef"],
        ["aab", "aba", "baa"],
        ["abcab", "bcabc", "cabca"],
    ]
    for words in examples:
        plural = "" if len(words) == 1 else "s"
        print(f"{len(words)} word{plural}: {verdict(words)}")
    count = 0
    letters = 0
    check = 0
    for _ in range(300):
        m = 1 + next_random() % 8
        alphabet = 2 + next_random() % 3
        raw = []
        for _ in range(m):
            length = 1 + next_random() % 6
            raw.append(random_word(length, alphabet))
        words = without_inside(raw)
        s = shortest_superstring(words)
        ok = True
        for w in words:
            if w not in s:
                ok = False
            letters += len(w)
        count += len(words)
        if not ok:
            print("WRONG")
        check = (check * 31 + len(s)) % 1000000007
    print(f"300 random sets of {count} words of {letters} letters: checksum {check}")
    sets = []
    ab = []
    while len(ab) < 12:
        ab.append(random_word(20, 2))
        ab = without_inside(ab)
    sets.append(ab)
    long = random_word(31, 26)
    sets.append([long[(k * 5) % 12:(k * 5) % 12 + 20] for k in range(12)])
    sets.append([chr(97 + k) * 20 for k in range(12)])
    sets.append([random_word(20, 26) for _ in range(12)])
    for words in sets:
        print(f"{len(words)} words of 20 letters: {verdict(words)}")


main()
