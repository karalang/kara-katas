"""Benchmark harness for LeetCode #291 — Word Pattern II backtracking.

Mirrors word_pattern_ii.kara algorithm-for-algorithm.
"""

NP = 8
SL = 30
ITERS = 500


def matches(p, pi, s, si, m, used):
    if pi >= len(p):
        return si >= len(s)
    if si >= len(s):
        return False

    key = p[pi : pi + 1]
    bound = m.get(key)
    if bound is not None:
        blen = len(bound)
        if si + blen > len(s):
            return False
        if s[si : si + blen] != bound:
            return False
        return matches(p, pi + 1, s, si + blen, m, used)

    end = si + 1
    while end <= len(s):
        cand = s[si:end]
        if cand not in used:
            m[key] = cand
            used.add(cand)
            if matches(p, pi + 1, s, end, m, used):
                return True
            del m[key]
            used.discard(cand)
        end += 1
    return False


def word_pattern_match(p, s):
    return matches(p, 0, s, 0, {}, set())


def main():
    alpha = ["a", "b", "c", "d"]
    subjects = []
    for j in range(NP):
        chars = []
        for k in range(SL):
            kk = k % (SL // 2) if j % 2 == 0 else k
            chars.append(alpha[(kk * 7 + j * 3) % 4])
        subjects.append("".join(chars))

    pat = "abcabc"
    sink = 0
    for it in range(ITERS):
        idx = (it * 5) % NP
        if word_pattern_match(pat, subjects[idx]):
            sink += it + 1
        else:
            sink += 1
    print(sink)


if __name__ == "__main__":
    main()
