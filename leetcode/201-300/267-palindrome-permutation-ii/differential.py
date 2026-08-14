"""LeetCode 267 — differential harness (Python mirror / oracle).

Mirrors differential.kara draw-for-draw: the same LCG, the same order of seed
advances, the same six families and the same shuffle, so the printed digest
must match byte for byte.
"""

MASK = 2147483647
DIGEST_MOD = 1000000007


def is_pal(a):
    i, j = 0, len(a) - 1
    while i < j:
        if a[i] != a[j]:
            return False
        i += 1
        j -= 1
    return True


def next_perm(a):
    n = len(a)
    if n < 2:
        return False
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i < 0:
        return False
    j = n - 1
    while a[j] <= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    a[i + 1:] = reversed(a[i + 1:])
    return True


def counts_of(chars):
    counts = [0] * 128
    for c in chars:
        counts[c] += 1
    return counts


def build(counts, half, half_len, middle, out):
    if len(half) == half_len:
        s = "".join(chr(c) for c in half)
        if middle >= 0:
            s += chr(middle)
        s += "".join(chr(c) for c in reversed(half))
        out.append(s)
        return
    for c in range(128):
        if counts[c] > 0:
            counts[c] -= 1
            half.append(c)
            build(counts, half, half_len, middle, out)
            half.pop()
            counts[c] += 1


def gen_backtrack(chars):
    counts = counts_of(chars)
    odd, middle, half_len = 0, -1, 0
    for c in range(128):
        if counts[c] % 2 == 1:
            odd += 1
            middle = c
        counts[c] //= 2
        half_len += counts[c]
    out = []
    if odd > 1:
        return out
    build(counts, [], half_len, middle, out)
    return out


def gen_iter(chars):
    counts = counts_of(chars)
    odd, middle = 0, -1
    half = []
    for c in range(128):
        if counts[c] % 2 == 1:
            odd += 1
            middle = c
        half.extend([c] * (counts[c] // 2))
    out = []
    if odd > 1:
        return out
    while True:
        s = "".join(chr(c) for c in half)
        if middle >= 0:
            s += chr(middle)
        s += "".join(chr(c) for c in reversed(half))
        out.append(s)
        if not next_perm(half):
            break
    return out


def gen_brute(chars):
    a = sorted(chars)
    out = []
    if not a:
        out.append("")
        return out
    if is_pal(a):
        out.append("".join(chr(c) for c in a))
    while next_perm(a):
        if is_pal(a):
            out.append("".join(chr(c) for c in a))
    return out


def multinomial(chars):
    counts = counts_of(chars)
    odd, half_len = 0, 0
    for c in range(128):
        if counts[c] % 2 == 1:
            odd += 1
        half_len += counts[c] // 2
    if odd > 1:
        return -1
    num = 1
    for k in range(2, half_len + 1):
        num *= k
    for d in range(128):
        h = counts[d] // 2
        f = 1
        for m in range(2, h + 1):
            f *= m
        num //= f
    return num


def main():
    cases = 2500
    seed = 267267

    mismatches = brute_checked = brute_disagree = 0
    count_disagree = nonempty = total_results = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & MASK
        family = (seed // 65536) % 6

        chars = []

        if family <= 1:
            alpha = family + 2
            seed = (seed * 1103515245 + 12345) & MASK
            n = (seed // 65536) % 9
            for _i in range(n):
                seed = (seed * 1103515245 + 12345) & MASK
                chars.append(97 + (seed // 65536) % alpha)
        if family == 2 or family == 3:
            pairs, alpha = (5, 4) if family == 3 else (3, 3)
            seed = (seed * 1103515245 + 12345) & MASK
            np_ = (seed // 65536) % (pairs + 1)
            for _i in range(np_):
                seed = (seed * 1103515245 + 12345) & MASK
                ch = 97 + (seed // 65536) % alpha
                chars.append(ch)
                chars.append(ch)
            seed = (seed * 1103515245 + 12345) & MASK
            if (seed // 65536) % 2 == 1:
                seed = (seed * 1103515245 + 12345) & MASK
                chars.append(97 + (seed // 65536) % alpha)
        if family == 4:
            seed = (seed * 1103515245 + 12345) & MASK
            np_ = (seed // 65536) % 3 + 1
            for _i in range(np_):
                seed = (seed * 1103515245 + 12345) & MASK
                ch = 97 + (seed // 65536) % 3
                chars.append(ch)
                chars.append(ch)
            seed = (seed * 1103515245 + 12345) & MASK
            at = (seed // 65536) % len(chars)
            seed = (seed * 1103515245 + 12345) & MASK
            chars[at] = 97 + (seed // 65536) % 3
        if family == 5:
            seed = (seed * 1103515245 + 12345) & MASK
            n = (seed // 65536) % 9
            seed = (seed * 1103515245 + 12345) & MASK
            ch = 97 + (seed // 65536) % 3
            chars.extend([ch] * n)

        m = len(chars)
        sh = m - 1
        while sh > 0:
            seed = (seed * 1103515245 + 12345) & MASK
            j = (seed // 65536) % (sh + 1)
            chars[sh], chars[j] = chars[j], chars[sh]
            sh -= 1

        a = gen_backtrack(chars)
        b = gen_iter(chars)
        if a != b:
            mismatches += 1

        if m <= 8:
            brute_checked += 1
            if a != gen_brute(chars):
                brute_disagree += 1

        want = multinomial(chars)
        got = len(a)
        if want < 0:
            if got != 0:
                count_disagree += 1
        elif got != want:
            count_disagree += 1

        if got > 0:
            nonempty += 1
        total_results += got
        h = 0
        for s in a:
            for ch in s.encode():
                h = (h * 31 + ch) % DIGEST_MOD
        digest = (digest * 131 + h + got) % DIGEST_MOD

    print(f"cases {cases}")
    print(f"non-empty answers {nonempty}")
    print(f"palindromes generated {total_results}")
    print(f"brute-force verified {brute_checked}")
    print(f"brute-force disagreements {brute_disagree}")
    print(f"multinomial disagreements {count_disagree}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


main()
