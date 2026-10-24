# LeetCode #966: Vowel Spellchecker -- three maps.
#
# Mirrors spellchecker.kara: one lookup per rule, in the rules' order:
# the words themselves in a set, then each word's lowercase form and its
# lowercase form with every vowel blanked out in maps to the first word
# that has it.


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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ",".join('"' + s + '"' for s in v) + "]"


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


def tally(qs, got, by_rule):
    for q, g in zip(qs, got):
        if g == q:
            rule = 0
        elif len(g) == 0:
            rule = 3
        elif g.lower() == q.lower():
            rule = 1
        else:
            rule = 2
        by_rule[rule] += 1


def main():
    global seed
    print(show(spellchecker(
        ["KiTe", "kite", "hare", "Hare"],
        ["kite", "Kite", "KiTe", "Hare", "HARE", "Hear", "hear", "keti", "keet", "keto"],
    )))
    print(show(spellchecker(["yellow"], ["YellOw"])))
    print(show(spellchecker(["a", "A", "e"], ["A", "E", "i", "b", "a"])))
    print(show(spellchecker(["zeo", "Zuo"], ["zuo", "ZEO", "zoe", "zo", "zeoo"])))
    print(show(spellchecker(
        ["AaAa", "aaaa", "uuuu", "UUUU"],
        ["aaaa", "AAAA", "uUuU", "ieao", "AAA", "aaaaa"],
    )))
    print(show(spellchecker(["bcd"], ["BCD", "bcd", "bad", "bcdd"])))
    seed = 966
    by_rule = [0, 0, 0, 0]
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 12
        m = 1 + next_random() % 12
        wl, qs = random_case(n, m, 4)
        got = spellchecker(wl, qs)
        tally(qs, got, by_rule)
        for g in got:
            check = fold(g, check)
    print(f"300 random cases: {by_rule[0]} words, {by_rule[1]} by case, {by_rule[2]} by vowels, {by_rule[3]} unmatched, checksum {check}")
    wl, qs = random_case(5000, 5000, 7)
    got = spellchecker(wl, qs)
    big = [0, 0, 0, 0]
    tally(qs, got, big)
    big_check = 0
    for g in got:
        big_check = fold(g, big_check)
    print(f"5000 words, 5000 queries: {big[0]} words, {big[1]} by case, {big[2]} by vowels, {big[3]} unmatched, checksum {big_check}")


main()
