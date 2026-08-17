#!/usr/bin/env python3
"""LeetCode 278 — differential harness. Mirror of differential.kara.

Two oracles, because the answer is not unique:
  * Kahn vs brute — string equality (both are the lexicographically smallest).
  * DFS — validation against the words, since reverse postorder yields *a*
    valid order and no visit order makes it the lex-smallest in general.
"""


def solve_kahn(words):
    present = [False] * 26
    indeg = [0] * 26
    adj = [False] * 676
    for w in words:
        for ch in w.encode():
            present[ch - 97] = True
    for p in range(len(words) - 1):
        a, c = words[p].encode(), words[p + 1].encode()
        found = False
        for k in range(min(len(a), len(c))):
            if a[k] != c[k]:
                u, v = a[k] - 97, c[k] - 97
                if not adj[u * 26 + v]:
                    adj[u * 26 + v] = True
                    indeg[v] += 1
                found = True
                break
        if not found and len(a) > len(c):
            return ""
    out = []
    done = [False] * 26
    remaining = sum(1 for r in range(26) if present[r])
    while remaining > 0:
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
            if adj[pick * 26 + t]:
                indeg[t] -= 1
        remaining -= 1
    return "".join(out)


def _graph(words):
    present = [False] * 26
    adj = [False] * 676
    for w in words:
        for ch in w.encode():
            present[ch - 97] = True
    for p in range(len(words) - 1):
        a, c = words[p].encode(), words[p + 1].encode()
        found = False
        for k in range(min(len(a), len(c))):
            if a[k] != c[k]:
                adj[(a[k] - 97) * 26 + (c[k] - 97)] = True
                found = True
                break
        if not found and len(a) > len(c):
            return None, None
    return present, adj


def solve_dfs(words):
    present, adj = _graph(words)
    if present is None:
        return ""
    colour = [0] * 26
    rev = []
    for root in range(26):
        if present[root] and colour[root] == 0:
            st, ix = [root], [0]
            colour[root] = 1
            while st:
                top = st[-1]
                t = ix[-1]
                advanced = False
                while t < 26 and not advanced:
                    if adj[top * 26 + t]:
                        if colour[t] == 1:
                            return ""
                        if colour[t] == 0:
                            ix[-1] = t + 1
                            colour[t] = 1
                            st.append(t)
                            ix.append(0)
                            advanced = True
                    if not advanced:
                        t += 1
                if not advanced:
                    colour[top] = 2
                    rev.append(top)
                    st.pop()
                    ix.pop()
    return "".join(chr(c + 97) for c in reversed(rev))


def words_ordered_under(words, rank):
    for p in range(len(words) - 1):
        a, c = words[p].encode(), words[p + 1].encode()
        decided, ok = False, True
        for k in range(min(len(a), len(c))):
            if a[k] != c[k]:
                decided = True
                if rank[a[k] - 97] > rank[c[k] - 97]:
                    ok = False
                break
        if not decided and len(a) > len(c):
            ok = False
        if not ok:
            return False
    return True


def solve_brute(words):
    present = [False] * 26
    for w in words:
        for ch in w.encode():
            present[ch - 97] = True
    letters = [c for c in range(26) if present[c]]
    perm = list(letters)
    while True:
        rank = [0] * 26
        for j, c in enumerate(perm):
            rank[c] = j
        if words_ordered_under(words, rank):
            return "".join(chr(c + 97) for c in perm)
        p = len(perm) - 2
        while p >= 0 and perm[p] >= perm[p + 1]:
            p -= 1
        if p < 0:
            return ""
        s = len(perm) - 1
        while perm[s] <= perm[p]:
            s -= 1
        perm[p], perm[s] = perm[s], perm[p]
        perm[p + 1:] = reversed(perm[p + 1:])


def is_valid_answer(words, ans):
    present = [False] * 26
    seen = [False] * 26
    for w in words:
        for ch in w.encode():
            present[ch - 97] = True
    rank = [-1] * 26
    for k, ch in enumerate(ans.encode()):
        c = ch - 97
        if not present[c] or seen[c]:
            return False
        seen[c] = True
        rank[c] = k
    for c in range(26):
        if present[c] and not seen[c]:
            return False
    return words_ordered_under(words, rank)


def pair_ok(x, y, rank):
    a, c = x.encode(), y.encode()
    for k in range(min(len(a), len(c))):
        if a[k] != c[k]:
            return rank[a[k] - 97] <= rank[c[k] - 97]
    return len(a) <= len(c)


def has_prefix_violation(words):
    for p in range(len(words) - 1):
        a, c = words[p].encode(), words[p + 1].encode()
        differs = any(a[k] != c[k] for k in range(min(len(a), len(c))))
        if not differs and len(a) > len(c):
            return True
    return False


def main():
    cases = satisfiable = invalid_cycle = invalid_prefix = 0
    kahn_vs_brute = dfs_invalid = existence_disagreements = 0
    dfs_differed_from_kahn = digest = 0

    seed = 20260817
    for alpha in range(2, 6):
        for t in range(300):
            nwords = 2 + (t % 4)
            words = []
            for _ in range(nwords):
                seed = (seed * 1103515245 + 12345) % 2147483648
                wlen = 1 + (seed // 7) % 3
                s = ""
                for _ in range(wlen):
                    seed = (seed * 1103515245 + 12345) % 2147483648
                    s += chr(97 + (seed // 11) % alpha)
                words.append(s)

            if t % 3 == 0:
                rank = [0] * 26
                for q in range(alpha):
                    rank[(alpha - 1) - q] = q
                a2 = 1
                while a2 < len(words):
                    b2 = a2
                    while b2 > 0 and not pair_ok(words[b2 - 1], words[b2], rank):
                        words[b2 - 1], words[b2] = words[b2], words[b2 - 1]
                        b2 -= 1
                    a2 += 1

            k_ans = solve_kahn(words)
            d_ans = solve_dfs(words)
            b_ans = solve_brute(words)

            if k_ans != b_ans:
                kahn_vs_brute += 1
            ke, de, be = (len(k_ans) == 0), (len(d_ans) == 0), (len(b_ans) == 0)
            if ke != be or de != be:
                existence_disagreements += 1
            if not de:
                if not is_valid_answer(words, d_ans):
                    dfs_invalid += 1
                if d_ans != k_ans:
                    dfs_differed_from_kahn += 1
            if be:
                if has_prefix_violation(words):
                    invalid_prefix += 1
                else:
                    invalid_cycle += 1
            else:
                satisfiable += 1
            digest = (digest * 131 + len(b_ans) + 7) % 1000000007
            cases += 1

    print(f"cases {cases}")
    print(f"satisfiable {satisfiable}")
    print(f"unsatisfiable by CYCLE {invalid_cycle}, by the PREFIX RULE {invalid_prefix}")
    print(f"DFS answers that differed from the lex-smallest {dfs_differed_from_kahn}")
    print(f"DFS answers that failed VALIDATION {dfs_invalid}")
    print(f"digest {digest}")
    print(f"kahn vs brute, as strings {kahn_vs_brute}")
    print(f"existence disagreements {existence_disagreements}")


main()
