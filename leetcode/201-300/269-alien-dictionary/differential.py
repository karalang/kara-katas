"""LeetCode 269 — differential harness (Python mirror / oracle).

Mirrors differential.kara draw-for-draw: the same LCG, the same order of seed
advances, the same five families and the same hidden-alphabet sort, so the
printed digest must match byte for byte.

Each solver derives its own constraints, deliberately duplicated — see the
comment in the .kara file for the measurement that justifies it.
"""

MASK = 2147483647
DIGEST_MOD = 1000000007


def word_of(chars):
    return "".join(chr(c + 97) for c in chars)


def before(a, b, rank):
    for k in range(min(len(a), len(b))):
        if a[k] != b[k]:
            return rank[a[k]] < rank[b[k]]
    return len(a) <= len(b)


def letters_of(words):
    present = [False] * 26
    for w in words:
        for b in w.encode():
            present[b - 97] = True
    return present


def _pairs(words):
    """Returns (lo, hi, ok). ok=False means a prefix violation."""
    lo, hi = [], []
    for p in range(len(words) - 1):
        a = [b - 97 for b in words[p].encode()]
        c = [b - 97 for b in words[p + 1].encode()]
        found = False
        for k in range(min(len(a), len(c))):
            if a[k] != c[k]:
                lo.append(a[k])
                hi.append(c[k])
                found = True
                break
        if not found and len(a) > len(c):
            return lo, hi, False
    return lo, hi, True


def kahn(words):
    present = letters_of(words)
    lo, hi, ok = _pairs(words)
    if not ok:
        return ""
    indeg = [0] * 26
    adj = [[False] * 26 for _ in range(26)]
    for e in range(len(lo)):
        if not adj[lo[e]][hi[e]]:
            adj[lo[e]][hi[e]] = True
            indeg[hi[e]] += 1
    done = [False] * 26
    remaining = sum(1 for d in range(26) if present[d])
    out = []
    while len(out) < remaining:
        pick = -1
        for s in range(26):
            if present[s] and not done[s] and indeg[s] == 0:
                pick = s
                break
        if pick < 0:
            return ""
        done[pick] = True
        out.append(chr(pick + 97))
        for t in range(26):
            if adj[pick][t]:
                indeg[t] -= 1
    return "".join(out)


def dfs(words):
    present = letters_of(words)
    lo, hi, ok0 = _pairs(words)
    if not ok0:
        return ""
    adj = [[False] * 26 for _ in range(26)]
    for e in range(len(lo)):
        adj[lo[e]][hi[e]] = True
    state = [0] * 26
    order = []
    ok = [True]

    def visit(u):
        state[u] = 1
        for v in range(26):
            if adj[u][v]:
                if state[v] == 1:
                    ok[0] = False
                elif state[v] == 0:
                    visit(v)
        state[u] = 2
        order.append(u)

    for u in range(26):
        if present[u] and state[u] == 0:
            visit(u)
    if not ok[0]:
        return ""
    return "".join(chr(c + 97) for c in reversed(order))


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


def brute(words):
    present = letters_of(words)
    lo, hi, ok = _pairs(words)
    if not ok:
        return ""
    letters = [s for s in range(26) if present[s]]
    if not letters:
        return ""
    while True:
        pos = [-1] * 26
        for q, L in enumerate(letters):
            pos[L] = q
        if all(pos[lo[e]] < pos[hi[e]] for e in range(len(lo))):
            return "".join(chr(c + 97) for c in letters)
        if not next_perm(letters):
            break
    return ""


def valid_order(words, cand):
    present = letters_of(words)
    lo, hi, ok = _pairs(words)
    if not ok:
        return False
    pos = [-1] * 26
    for idx, b in enumerate(cand.encode()):
        c = b - 97
        if pos[c] >= 0:
            return False
        pos[c] = idx
    for s in range(26):
        if present[s] and pos[s] < 0:
            return False
        if not present[s] and pos[s] >= 0:
            return False
    return all(pos[lo[e]] < pos[hi[e]] for e in range(len(lo)))


def main():
    cases = 1500
    seed = 269269

    star_vs_brute = dfs_verdict = dfs_invalid = 0
    solvable = prefix_rejects = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & MASK
        family = (seed // 65536) % 5

        seed = (seed * 1103515245 + 12345) & MASK
        k = (seed // 65536) % 5 + 2
        seed = (seed * 1103515245 + 12345) & MASK
        m = (seed // 65536) % 6 + 1

        alpha = list(range(k))
        sh = k - 1
        while sh > 0:
            seed = (seed * 1103515245 + 12345) & MASK
            j = (seed // 65536) % (sh + 1)
            alpha[sh], alpha[j] = alpha[j], alpha[sh]
            sh -= 1
        rank = [0] * 26
        for r0 in range(k):
            rank[alpha[r0]] = r0

        raw = []
        for _w in range(m):
            seed = (seed * 1103515245 + 12345) & MASK
            ln = (seed // 65536) % 4 + 1
            wd = []
            for _p in range(ln):
                seed = (seed * 1103515245 + 12345) & MASK
                wd.append((seed // 65536) % k)
            raw.append(wd)

        if family <= 2:
            a = 1
            while a < len(raw):
                b = a
                while b > 0 and not before(raw[b - 1], raw[b], rank):
                    raw[b], raw[b - 1] = raw[b - 1], raw[b]
                    b -= 1
                a += 1
        if family == 1 and len(raw) >= 2:
            seed = (seed * 1103515245 + 12345) & MASK
            at = (seed // 65536) % (len(raw) - 1)
            raw[at], raw[at + 1] = raw[at + 1], raw[at]
        if family == 2 and len(raw) >= 1:
            src = raw[0]
            if len(src) >= 2:
                pre = src[:-1]
                raw.append(pre)
                fixed = [src, raw[len(raw) - 1]]
                for rest in range(1, len(raw) - 1):
                    fixed.append(raw[rest])
                raw = fixed

        words = [word_of(r) for r in raw]

        a1 = kahn(words)
        a2 = brute(words)
        a3 = dfs(words)

        if a1 != a2:
            star_vs_brute += 1
        e1 = a1 == ""
        e3 = a3 == ""
        if e1 != e3:
            dfs_verdict += 1
        if not e3 and not valid_order(words, a3):
            dfs_invalid += 1

        if a1 != "":
            solvable += 1
        if not _pairs(words)[2]:
            prefix_rejects += 1

        for ch in a1.encode():
            digest = (digest * 31 + ch) % DIGEST_MOD
        digest = (digest * 131 + len(words)) % DIGEST_MOD

    print(f"cases {cases}")
    print(f"solvable {solvable}")
    print(f"rejected by the prefix rule {prefix_rejects}")
    print(f"digest {digest}")
    print(f"star vs brute mismatches {star_vs_brute}")
    print(f"dfs verdict mismatches {dfs_verdict}")
    print(f"dfs invalid orders {dfs_invalid}")


main()
