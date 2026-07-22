"""LeetCode 205 — Isomorphic Strings (Python mirror / oracle).

Bijection check via two maps: s->t catches inconsistent forward mapping, t->s
catches two sources colliding on one target. Mirrors the Kāra version.
"""


def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    st = {}
    ts = {}
    for a, b in zip(s, t):
        if a in st:
            if st[a] != b:
                return False
        else:
            st[a] = b
        if b in ts:
            if ts[b] != a:
                return False
        else:
            ts[b] = a
    return True


def report(s, t):
    print("true" if is_isomorphic(s, t) else "false")


def main():
    report("egg", "add")
    report("foo", "bar")
    report("paper", "title")
    report("badc", "baba")
    report("", "")
    report("ab", "aa")
    report("abcabc", "xyzxyz")


main()
