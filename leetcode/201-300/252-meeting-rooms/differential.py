"""LeetCode 252 - differential harness. Python oracle.

Mirrors differential.kara exactly: same LCG, same three case families, same
shuffle, the same three deciders and the same census.

Durations are drawn >= 1 deliberately. LeetCode constrains 0 <= start < end,
and a zero-length interval breaks the sort-and-compare-adjacent decider while
the pairwise definition absorbs it -- see the README. Generating out-of-spec
input made the three deciders disagree on 8.9% of cases.
"""


def make_case(seed):
    state = seed
    out = []
    state = (state * 1103515245 + 12345) & 2147483647
    n = (state // 65536) % 9
    if n == 0:
        return out
    state = (state * 1103515245 + 12345) & 2147483647
    family = (state // 65536) % 4

    if family <= 1:
        cursor = 0
        for _ in range(n):
            state = (state * 1103515245 + 12345) & 2147483647
            dur = (state // 65536) % 5 + 1
            state = (state * 1103515245 + 12345) & 2147483647
            gap = (state // 65536) % 3 // 2
            out.append((cursor, cursor + dur))
            cursor = cursor + dur + gap
    elif family == 2:
        cursor = 0
        for _ in range(n):
            state = (state * 1103515245 + 12345) & 2147483647
            dur = (state // 65536) % 5 + 1
            out.append((cursor, cursor + dur))
            cursor += dur
        state = (state * 1103515245 + 12345) & 2147483647
        victim = (state // 65536) % n
        if victim > 0:
            v = out[victim]
            out[victim] = (v[0] - 1, v[1])
    else:
        for _ in range(n):
            state = (state * 1103515245 + 12345) & 2147483647
            s = (state // 65536) % 40
            state = (state * 1103515245 + 12345) & 2147483647
            d = (state // 65536) % 8 + 1
            out.append((s, s + d))

    k = len(out) - 1
    while k > 0:
        state = (state * 1103515245 + 12345) & 2147483647
        swap = (state // 65536) % (k + 1)
        out[k], out[swap] = out[swap], out[k]
        k -= 1
    return out


def decide_sorted(iv):
    s = sorted(iv, key=lambda x: x[0])
    for k in range(1, len(s)):
        if s[k][0] < s[k - 1][1]:
            return False
    return True


def decide_sweep(iv):
    n = len(iv)
    if n <= 1:
        return True
    starts = sorted(x[0] for x in iv)
    ends = sorted(x[1] for x in iv)
    j = 0
    active = 0
    for k in range(n):
        while j < n and ends[j] <= starts[k]:
            active -= 1
            j += 1
        active += 1
        if active > 1:
            return False
    return True


def decide_pairwise(iv):
    n = len(iv)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = iv[i], iv[j]
            if max(a[0], b[0]) < min(a[1], b[1]):
                return False
    return True


def main():
    cases = 1200
    seed = 252252
    yes = no = mismatches = touching = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & 2147483647
        iv = make_case(seed)

        a = decide_sorted(iv)
        b = decide_sweep(iv)
        d = decide_pairwise(iv)

        if a != b or a != d:
            mismatches += 1
        if a:
            yes += 1
            digest = (digest * 131 + 1) % 1000000007
        else:
            no += 1
            digest = (digest * 131) % 1000000007

        s = sorted(iv, key=lambda x: x[0])
        if any(s[u][0] == s[u - 1][1] for u in range(1, len(s))):
            touching += 1

    print(f"cases {cases}")
    print(f"attendable {yes}")
    print(f"clashing {no}")
    print(f"with touching boundary {touching}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


if __name__ == "__main__":
    main()
