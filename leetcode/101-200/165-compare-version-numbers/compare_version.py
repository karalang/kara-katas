"""LeetCode 165 — Compare Version Numbers (Python mirror / oracle).

Parse each version into its list of integer revisions (leading zeros
insignificant), then compare element by element padding the shorter with zeros.
Mirrors the Kāra version (digit-accumulation parse, no library split-to-int).
"""


def revisions(v):
    revs = []
    val = 0
    i = 0
    n = len(v)
    while i < n:
        val = 0
        while i < n and v[i] != ".":
            val = val * 10 + (ord(v[i]) - ord("0"))
            i += 1
        revs.append(val)
        i += 1
    return revs


def compare_version(v1, v2):
    a = revisions(v1)
    b = revisions(v2)
    m = max(len(a), len(b))
    for i in range(m):
        x = a[i] if i < len(a) else 0
        y = b[i] if i < len(b) else 0
        if x < y:
            return -1
        if x > y:
            return 1
    return 0


def report(v1, v2):
    print(compare_version(v1, v2))


def main():
    report("1.2", "1.10")
    report("1.01", "1.001")
    report("1.0", "1.0.0.0")
    report("1.0.1", "1")
    report("7.5.2.4", "7.5.3")
    report("1.1", "1.1")
    report("0.1", "1.1")
    report("1.0.0", "1")
    report("12.34", "12.3")


main()
