"""Benchmark workload for LeetCode #253 — Meeting Rooms II (Python; scale lane)."""


def heap_push(h, v):
    h.append(v)
    i = len(h) - 1
    while i > 0:
        p = (i - 1) // 2
        if h[i] < h[p]:
            h[i], h[p] = h[p], h[i]
            i = p
        else:
            break


def heap_pop(h):
    n = len(h)
    if n == 0:
        return
    last = h.pop()
    if n == 1:
        return
    h[0] = last
    m = len(h)
    i = 0
    while True:
        l, r = 2 * i + 1, 2 * i + 2
        sm = i
        if l < m and h[l] < h[sm]:
            sm = l
        if r < m and h[r] < h[sm]:
            sm = r
        if sm == i:
            break
        h[i], h[sm] = h[sm], h[i]
        i = sm


def main():
    n = 150000
    rounds = 25

    base = []
    state = 253253
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        jitter = (state // 65536) % 8
        state = (state * 1103515245 + 12345) & 2147483647
        dur = (state // 65536) % 60 + 1
        s = i + jitter
        base.append((s, s + dur))
    for k in range(n - 1, 0, -1):
        state = (state * 1103515245 + 12345) & 2147483647
        sw = (state // 65536) % (k + 1)
        base[k], base[sw] = base[sw], base[k]

    sink = 0
    for _ in range(rounds):
        s = sorted(base, key=lambda x: x[0])
        h = []
        rooms = 0
        for j in range(n):
            while h and h[0] <= s[j][0]:
                heap_pop(h)
            heap_push(h, s[j][1])
            if len(h) > rooms:
                rooms = len(h)
        sink = (sink * 31 + rooms) % 1000000007
    print(sink)


main()
