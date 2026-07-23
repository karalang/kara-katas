"""Benchmark workload for LeetCode #207 — Course Schedule (Python; scale lane)."""


def main():
    n = 5000
    m = 15000
    passes = 8000

    esrc = [0] * m
    edst = [0] * m
    state = 12345
    for e in range(m):
        state = (state * 1103515245 + 12345) & 2147483647
        s = state % n
        state = (state * 1103515245 + 12345) & 2147483647
        d = state % n
        esrc[e] = s
        edst[e] = d

    outdeg = [0] * n
    base_indeg = [0] * n
    for e in range(m):
        outdeg[esrc[e]] += 1
        base_indeg[edst[e]] += 1

    offset = [0] * (n + 1)
    acc = 0
    for c in range(n):
        acc += outdeg[c]
        offset[c + 1] = acc

    adj = [0] * m
    cursor = [0] * n
    for c in range(n):
        cursor[c] = offset[c]
    for e in range(m):
        sidx = cursor[esrc[e]]
        adj[sidx] = edst[e]
        cursor[esrc[e]] = sidx + 1

    indeg = [0] * n
    queue = [0] * n

    sink = 0
    for p in range(passes):
        for c in range(n):
            indeg[c] = base_indeg[c]
        blocked = p % n
        indeg[blocked] += 1

        qt = 0
        for c in range(n):
            if indeg[c] == 0:
                queue[qt] = c
                qt += 1

        qh = 0
        finished = 0
        while qh < qt:
            node = queue[qh]
            qh += 1
            finished += 1
            stop = offset[node + 1]
            k = offset[node]
            while k < stop:
                nb = adj[k]
                indeg[nb] -= 1
                if indeg[nb] == 0:
                    queue[qt] = nb
                    qt += 1
                k += 1
        sink += finished
    print(sink)


main()
