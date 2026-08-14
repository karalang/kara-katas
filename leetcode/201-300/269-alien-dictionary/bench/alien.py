"""Benchmark workload for LeetCode #269 — Alien Dictionary (Python mirror).

Mirrors alien.kara algorithm-for-algorithm, including the flat corpus and the
hoisted working structures. Correctness oracle only — Python is not a measured
lane (see BENCHMARKS.md).

NOTE ON VERIFICATION: at the real parameters this is 1,200,000 solver calls and
is not practical to run to completion. It is verified against the kāra binary at
a reduced `rounds`, which is sound: the per-list `acc` values do not depend on
`rounds` at all, and the sink is a deterministic fold over identical passes, so
agreement at a small round count is agreement at any.
"""

LISTS = 20000
ROUNDS = 60
ALPHA = 8


def main():
    letters, wstart, wlen, lstart, lcount = [], [], [], [], []
    state = 269269

    for _ in range(LISTS):
        state = (state * 1103515245 + 12345) & 2147483647
        m = (state // 65536) % 5 + 2

        rank = list(range(ALPHA))
        sh = ALPHA - 1
        while sh > 0:
            state = (state * 1103515245 + 12345) & 2147483647
            j = (state // 65536) % (sh + 1)
            rank[sh], rank[j] = rank[j], rank[sh]
            sh -= 1

        buf, st, ln = [], [], []
        for _w in range(m):
            state = (state * 1103515245 + 12345) & 2147483647
            L = (state // 65536) % 4 + 1
            st.append(len(buf))
            ln.append(L)
            for _p in range(L):
                state = (state * 1103515245 + 12345) & 2147483647
                buf.append((state // 65536) % ALPHA)

        a = 1
        while a < m:
            b = a
            while b > 0:
                s1, n1 = st[b - 1], ln[b - 1]
                s2, n2 = st[b], ln[b]
                lim = min(n1, n2)
                k = 0
                swap = decided = False
                while k < lim:
                    if buf[s1 + k] != buf[s2 + k]:
                        if rank[buf[s1 + k]] > rank[buf[s2 + k]]:
                            swap = True
                        decided = True
                        k = lim
                    else:
                        k += 1
                if not decided and n1 > n2:
                    swap = True
                if swap:
                    st[b - 1], st[b] = st[b], st[b - 1]
                    ln[b - 1], ln[b] = ln[b], ln[b - 1]
                    b -= 1
                else:
                    b = 0
            a += 1

        state = (state * 1103515245 + 12345) & 2147483647
        if (state // 65536) % 2 == 0 and m >= 2:
            state = (state * 1103515245 + 12345) & 2147483647
            at = (state // 65536) % (m - 1)
            st[at], st[at + 1] = st[at + 1], st[at]
            ln[at], ln[at + 1] = ln[at + 1], ln[at]

        lstart.append(len(wstart))
        lcount.append(m)
        for q in range(m):
            wstart.append(len(letters))
            wlen.append(ln[q])
            for r in range(ln[q]):
                letters.append(buf[st[q] + r])

    adj = [False] * 676
    indeg = [0] * 26
    present = [False] * 26
    done = [False] * 26

    sink = 0
    for _r0 in range(ROUNDS):
        for idx in range(LISTS):
            base, n = lstart[idx], lcount[idx]

            for c in range(26):
                indeg[c] = 0
                present[c] = False
                done[c] = False
            for e in range(676):
                adj[e] = False

            for w in range(n):
                s, L = wstart[base + w], wlen[base + w]
                for p in range(L):
                    present[letters[s + p]] = True

            bad = False
            p2 = 0
            while p2 + 1 < n:
                s1, n1 = wstart[base + p2], wlen[base + p2]
                s2, n2 = wstart[base + p2 + 1], wlen[base + p2 + 1]
                lim = min(n1, n2)
                k = 0
                found = False
                while k < lim:
                    x, y = letters[s1 + k], letters[s2 + k]
                    if x != y:
                        if not adj[x * 26 + y]:
                            adj[x * 26 + y] = True
                            indeg[y] += 1
                        found = True
                        k = lim
                    else:
                        k += 1
                if not found and n1 > n2:
                    bad = True
                    p2 = n
                else:
                    p2 += 1

            acc = 0
            if not bad:
                remaining = sum(1 for d in range(26) if present[d])
                placed = 0
                while placed < remaining:
                    pick = -1
                    s3 = 0
                    while s3 < 26:
                        if present[s3] and not done[s3] and indeg[s3] == 0:
                            pick = s3
                            s3 = 26
                        else:
                            s3 += 1
                    if pick < 0:
                        acc = 0
                        placed = remaining
                    else:
                        done[pick] = True
                        acc = (acc * 31 + pick + 1) % 1000000007
                        placed += 1
                        for t in range(26):
                            if adj[pick * 26 + t]:
                                indeg[t] -= 1
            sink = (sink * 131 + acc) % 1000000007

    print(sink)


main()
