"""LeetCode 291 — Word Pattern II (reference oracle).

Same backtracking bijection search as the Kara version.
"""


def word_pattern_match(p, s):
    mapping = {}
    used = set()

    def matches(pi, si):
        if pi >= len(p):
            return si >= len(s)
        if si >= len(s):
            return False
        key = p[pi]
        if key in mapping:
            bound = mapping[key]
            if si + len(bound) > len(s):
                return False
            if s[si:si + len(bound)] != bound:
                return False
            return matches(pi + 1, si + len(bound))
        for end in range(si + 1, len(s) + 1):
            cand = s[si:end]
            if cand not in used:
                mapping[key] = cand
                used.add(cand)
                if matches(pi + 1, end):
                    return True
                del mapping[key]
                used.discard(cand)
        return False

    return matches(0, 0)


def report(p, s):
    print(f"{p} / {s} -> {str(word_pattern_match(p, s)).lower()}")


def main():
    report("abab", "redblueredblue")
    report("aaaa", "asdasdasdasd")
    report("aabb", "xyzabcxzyabc")
    report("ab", "aa")
    report("a", "a")
    report("abc", "xy")
    report("aba", "xyzxyzxyz")


if __name__ == "__main__":
    main()
