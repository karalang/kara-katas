"""Benchmark workload for LeetCode #210 — Course Schedule II (Python; scale lane)."""

MOD = 1000000007
BIG = 1000000


def main():
    n = 20000
    e = 80000
    passes = 800

    eb = []
    ea = []
    outdeg = [0] * n
    indeg0 = [0] * n

    state = 12345
    for _ in range(e):
        state = (state * 1103515245 + 12345) & 2147483647
        b = state % (n - 1)  # 0 .. n-2
        state = (state * 1103515245 + 12345) & 2147483647
        a = b + 1 + state % (n - 1 - b)  # b+1 .. n-1 (b < a => DAG)
        eb.append(b)
        ea.append(a)
        outdeg[b] += 1
        indeg0[a] += 1

    # CSR build.
    adj_start = [0] * (n + 1)
    for i in range(n):
        adj_start[i + 1] = adj_start[i] + outdeg[i]
    adj_flat = [0] * e
    cursor = adj_start[:n]
    for i in range(e):
        src = eb[i]
        adj_flat[cursor[src]] = ea[i]
        cursor[src] += 1

    indeg = [0] * n
    queue = [0] * n

    sink = 0
    for p in range(passes):
        for i in range(n):
            indeg[i] = indeg0[i]
        blocked = p % n
        indeg[blocked] += BIG

        head = 0
        tail = 0
        for c in range(n):
            if indeg[c] == 0:
                queue[tail] = c
                tail += 1
        checksum = 0
        cnt = 0
        while head < tail:
            node = queue[head]
            head += 1
            checksum = (checksum + node * (cnt + 1)) % MOD
            cnt += 1
            start = adj_start[node]
            end = adj_start[node + 1]
            for j in range(start, end):
                nb = adj_flat[j]
                indeg[nb] -= 1
                if indeg[nb] == 0:
                    queue[tail] = nb
                    tail += 1
        sink += cnt + checksum

    print(sink)


main()
