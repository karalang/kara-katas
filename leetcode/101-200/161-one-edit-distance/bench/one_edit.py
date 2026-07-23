"""Benchmark workload for LeetCode #161 — One Edit Distance (Python; scale lane)."""


def tails_equal(s, l, ss, se, ls, le):
    a = ss
    b = ls
    while a < se and b < le:
        if s[a] != l[b]:
            return False
        a += 1
        b += 1
    return a == se and b == le


def check(s, so, m, l, lo, n):
    if n - m > 1:
        return False
    i = 0
    while i < m:
        if s[so + i] != l[lo + i]:
            if m == n:
                return tails_equal(s, l, so + i + 1, so + m, lo + i + 1, lo + n)
            return tails_equal(s, l, so + i, so + m, lo + i + 1, lo + n)
        i += 1
    return n - m == 1


def is_one_edit(a, oa, la, b, ob, lb):
    if la <= lb:
        return check(a, oa, la, b, ob, lb)
    return check(b, ob, lb, a, oa, la)


def main():
    pairs = 4000
    l = 48
    reps = 3000
    stride = l + 2
    cap = pairs * stride

    buf_a = [0] * cap
    buf_b = [0] * cap
    len_a = [0] * pairs
    len_b = [0] * pairs

    state = 12345
    for pi in range(pairs):
        oa = pi * stride
        ob = pi * stride
        for k in range(l):
            state = (state * 1103515245 + 12345) & 2147483647
            buf_a[oa + k] = state % 26
        len_a[pi] = l
        state = (state * 1103515245 + 12345) & 2147483647
        kind = state % 4
        if kind == 0:
            for j in range(l):
                buf_b[ob + j] = buf_a[oa + j]
            state = (state * 1103515245 + 12345) & 2147483647
            pos = state % l
            buf_b[ob + pos] = (buf_a[oa + pos] + 1) % 26
            len_b[pi] = l
        elif kind == 1:
            state = (state * 1103515245 + 12345) & 2147483647
            pos = state % (l + 1)
            for j in range(pos):
                buf_b[ob + j] = buf_a[oa + j]
            state = (state * 1103515245 + 12345) & 2147483647
            buf_b[ob + pos] = state % 26
            for t in range(pos, l):
                buf_b[ob + t + 1] = buf_a[oa + t]
            len_b[pi] = l + 1
        elif kind == 2:
            state = (state * 1103515245 + 12345) & 2147483647
            pos = state % l
            w = 0
            for j in range(l):
                if j != pos:
                    buf_b[ob + w] = buf_a[oa + j]
                    w += 1
            len_b[pi] = l - 1
        else:
            for j in range(l):
                buf_b[ob + j] = buf_a[oa + j]
            state = (state * 1103515245 + 12345) & 2147483647
            p1 = state % l
            state = (state * 1103515245 + 12345) & 2147483647
            p2 = (p1 + 1 + state % (l - 1)) % l
            buf_b[ob + p1] = (buf_a[oa + p1] + 1) % 26
            buf_b[ob + p2] = (buf_a[oa + p2] + 1) % 26
            len_b[pi] = l

    sink = 0
    for rep in range(reps):
        idx = rep % pairs
        col = (rep * 7 + 3) % l
        oa = idx * stride
        buf_a[oa + col] = (buf_a[oa + col] + 1) % 26
        for i in range(pairs):
            o = i * stride
            if is_one_edit(buf_a, o, len_a[i], buf_b, o, len_b[i]):
                sink += 1
    print(sink)


main()
