"""LeetCode 266 — differential harness (Python mirror / oracle).

Mirrors differential.kara draw-for-draw: the same LCG, the same order of seed
advances, the same eight families and the same shuffle, so the printed digest
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


def brute(chars):
    a = sorted(chars)
    if is_pal(a):
        return True
    while next_perm(a):
        if is_pal(a):
            return True
    return False


def by_counts(chars):
    counts = [0] * 256
    for ch in chars:
        counts[ch] += 1
    return sum(1 for c in counts if c % 2 == 1) <= 1


def by_toggle(chars):
    odd = set()
    for ch in chars:
        if ch in odd:
            odd.discard(ch)
        else:
            odd.add(ch)
    return len(odd) <= 1


def by_bits(chars):
    mask = 0
    for ch in chars:
        mask ^= 1 << (ch - 97)
    return mask & (mask - 1) == 0


def main():
    cases = 4000
    seed = 266266

    mismatches = 0
    brute_checked = 0
    brute_disagreements = 0
    trues = 0
    even_len_true = 0
    digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & MASK
        family = (seed // 65536) % 8

        chars = []

        if family <= 3:
            alpha = family + 1
            seed = (seed * 1103515245 + 12345) & MASK
            n = (seed // 65536) % 8
            for _i in range(n):
                seed = (seed * 1103515245 + 12345) & MASK
                chars.append(97 + (seed // 65536) % alpha)
        if family == 4 or family == 5:
            pairs, alpha = (20, 8) if family == 5 else (3, 4)
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
        if family == 6:
            seed = (seed * 1103515245 + 12345) & MASK
            n = (seed // 65536) % 41
            for _i in range(n):
                seed = (seed * 1103515245 + 12345) & MASK
                chars.append(97 + (seed // 65536) % 8)
        if family == 7:
            seed = (seed * 1103515245 + 12345) & MASK
            np_ = (seed // 65536) % 4 + 1
            for _i in range(np_):
                seed = (seed * 1103515245 + 12345) & MASK
                ch = 97 + (seed // 65536) % 4
                chars.append(ch)
                chars.append(ch)
            seed = (seed * 1103515245 + 12345) & MASK
            at = (seed // 65536) % len(chars)
            seed = (seed * 1103515245 + 12345) & MASK
            chars[at] = 97 + (seed // 65536) % 4

        m = len(chars)
        sh = m - 1
        while sh > 0:
            seed = (seed * 1103515245 + 12345) & MASK
            j = (seed // 65536) % (sh + 1)
            chars[sh], chars[j] = chars[j], chars[sh]
            sh -= 1

        a = by_counts(chars)
        b = by_toggle(chars)
        d = by_bits(chars)
        if a != b or a != d:
            mismatches += 1

        if m <= 7:
            brute_checked += 1
            if brute(chars) != a:
                brute_disagreements += 1

        if a:
            trues += 1
        if a and m % 2 == 0:
            even_len_true += 1
        digest = (digest * 131 + (1 if a else 0) * 7 + m) % DIGEST_MOD

    print(f"cases {cases}")
    print(f"permutable {trues}")
    print(f"even length AND permutable {even_len_true}")
    print(f"brute-force verified {brute_checked}")
    print(f"brute-force disagreements {brute_disagreements}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


main()
