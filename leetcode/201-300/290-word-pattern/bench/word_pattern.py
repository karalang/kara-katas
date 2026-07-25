"""Benchmark harness for LeetCode #290 — Word Pattern.

Mirrors word_pattern.kara algorithm-for-algorithm, including the explicit
character-by-character split (rather than str.split) so the measured work
matches.
"""

NP = 8
PL = 1000
ALPHA_N = 26
ITERS = 2500


def split_words(s):
    words = []
    cur = []
    have = False
    for ch in s:
        if ch == " ":
            if have:
                words.append("".join(cur))
                cur = []
                have = False
        else:
            cur.append(ch)
            have = True
    if have:
        words.append("".join(cur))
    return words


def word_pattern(pattern, s):
    words = split_words(s)
    if len(pattern) != len(words):
        return False

    p2w = {}
    w2p = {}

    for i in range(len(pattern)):
        c = ord(pattern[i])
        w = words[i]

        prev = p2w.get(c)
        if prev is not None:
            if prev != w:
                return False
        else:
            p2w[c] = w

        pc = w2p.get(w)
        if pc is not None:
            if pc != c:
                return False
        else:
            w2p[w] = c
    return True


def main():
    alpha = [chr(97 + a) for a in range(ALPHA_N)]

    patterns = []
    subjects = []
    for j in range(NP):
        pat = []
        sub = []
        for i in range(PL):
            slot = (i + j) % ALPHA_N
            pat.append(alpha[slot])
            if i > 0:
                sub.append(" ")
            wslot = j % ALPHA_N if (j % 2 == 1 and i == PL - 1) else slot
            sub.append(f"w{wslot}")
        patterns.append("".join(pat))
        subjects.append("".join(sub))

    sink = 0
    for it in range(ITERS):
        idx = (it * 3) % NP
        if word_pattern(patterns[idx], subjects[idx]):
            sink += it + 1
        else:
            sink += 1
    print(sink)


if __name__ == "__main__":
    main()
