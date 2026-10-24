# Benchmark: LeetCode #966 Vowel Spellchecker -- the ★ arm, three maps,
# on cases of 5000 words and 5000 queries, LeetCode's largest. Mirrors
# spellchecker.kara, .c, .rs and go-seq/.


def devowel(w):
    return "".join("*" if c in "aeiou" else c for c in w.lower())


def spellchecker(wordlist, queries):
    exact = set(wordlist)
    by_case = {}
    by_vowel = {}
    for w in wordlist:
        by_case.setdefault(w.lower(), w)
        by_vowel.setdefault(devowel(w), w)
    out = []
    for q in queries:
        if q in exact:
            out.append(q)
        elif q.lower() in by_case:
            out.append(by_case[q.lower()])
        elif devowel(q) in by_vowel:
            out.append(by_vowel[devowel(q)])
        else:
            out.append("")
    return out



seed = 966


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


ALPHABET = "aeioukbAEIOUKB"


def spell(letters):
    return "".join(ALPHABET[x] for x in letters)


def random_word(length):
    return [next_random() % 14 for _ in range(length)]


def query_from(w, kind, max_len):
    if kind == 3:
        return random_word(1 + next_random() % max_len)
    q = list(w)
    for i in range(len(q)):
        if kind == 1 and next_random() % 2 == 0:
            q[i] = (q[i] + 7) % 14
        elif kind == 2 and q[i] % 7 < 5 and next_random() % 2 == 0:
            a = next_random() % 5
            q[i] = a + 7 * (next_random() % 2)
    return q


def fold(s, check):
    h = check
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return (h * 131 + 1) % 1000000007


def random_case(n, m, max_len):
    ws = []
    for _ in range(n):
        length = 1 + next_random() % max_len
        ws.append(random_word(length))
    qs = []
    for _ in range(m):
        w = ws[next_random() % n]
        kind = next_random() % 4
        qs.append(spell(query_from(w, kind, max_len)))
    return [spell(w) for w in ws], qs


def main():
    rounds = 200
    wls = []
    qss = []
    for _ in range(5):
        wl, qs = random_case(5000, 5000, 7)
        wls.append(wl)
        qss.append(qs)
    matched = 0
    check = 0
    for r in range(rounds):
        got = spellchecker(wls[r % 5], qss[r % 5])
        for g in got:
            if len(g) > 0:
                matched += 1
            check = fold(g, check)
    print(f"{rounds} rounds over 5 cases of 5000 words and 5000 queries: {matched} matched, checksum {check}")


main()
