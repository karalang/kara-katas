"""LeetCode 247 - Strobogrammatic Number II (reference oracle).

Return every strobogrammatic number of length n, in the order the recursion
produces them.

Build from the MIDDLE OUTWARD, not left to right. A strobogrammatic number of
length k is a legal outer pair wrapped around a strobogrammatic number of length
k-2, so the recursion bottoms out at k==0 ("") and k==1 ("0","1","8" - the three
digits that survive rotating in place, which is what may sit at an odd centre).

The one wrinkle is the leading zero. "0" wrapped in a 0-pair gives "000", which
is not a number. So the outermost layer - and only that layer, which is why n is
threaded through the recursion - refuses the 0/0 pair. Note n==1 is exempt: "0"
alone IS a valid answer.
"""

PAIRS = [("0", "0"), ("1", "1"), ("6", "9"), ("8", "8"), ("9", "6")]
ROT = {"0": "0", "1": "1", "8": "8", "6": "9", "9": "6"}


def build(k, n):
    if k == 0:
        return [""]
    if k == 1:
        return ["0", "1", "8"]
    inner = build(k - 2, n)
    out = []
    for s in inner:
        for a, b in PAIRS:
            if a == "0" and k == n:
                continue
            out.append(a + s + b)
    return out


def strobogrammatic(n):
    return build(n, n)


def is_strobogrammatic(num):
    lo, hi = 0, len(num) - 1
    while lo <= hi:
        a = num[lo]
        if a not in ROT or ROT[a] != num[hi]:
            return False
        lo += 1
        hi -= 1
    return True


def brute_force(n):
    """Every n-digit string, filtered by the #246 checker. Independent of the
    generator: enumeration + a predicate, versus construction. Leading zeros are
    excluded for n > 1, matching what "a number of length n" means."""
    out = []
    total = 10 ** n
    for v in range(total):
        s = str(v).rjust(n, "0")
        if n > 1 and s[0] == "0":
            continue
        if is_strobogrammatic(s):
            out.append(s)
    return out


def main():
    # `valid` re-checks every generated number with the #246 two-pointer
    # predicate - an independent confirmation that the generator emits only
    # strobogrammatic numbers, and one both language mirrors can run.
    for n in range(1, 8):
        got = strobogrammatic(n)
        valid = sum(1 for s in got if is_strobogrammatic(s))
        print(f"n={n} count={len(got)} valid={valid}")
        if n <= 3:
            print("  " + " ".join(got))


def verify():
    """Generator vs enumerate-and-filter, as sets - construction versus a
    predicate over every candidate. Python-only because brute force needs
    zero-padded integer formatting; run with `python3 strobogrammatic_ii.py
    --verify`. n<=5 keeps it at 100k candidates."""
    for n in range(1, 6):
        a = sorted(strobogrammatic(n))
        b = sorted(brute_force(n))
        print(f"n={n} generator == brute force: {'yes' if a == b else 'NO'}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        verify()
    else:
        main()
