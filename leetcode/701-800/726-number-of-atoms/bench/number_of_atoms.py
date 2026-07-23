"""Benchmark workload for LeetCode #726 — Number of Atoms (Python; scale lane)."""


def is_upper(b):
    return 65 <= b <= 90


def is_lower(b):
    return 97 <= b <= 122


def is_digit(b):
    return 48 <= b <= 57


def draw_hi(state):
    state = (state * 1103515245 + 12345) & 2147483647
    return state, state >> 16


def main():
    num_chunks = 20000
    passes = 400
    id_range = 24

    buf = bytearray()
    dpos = []
    state = 12345

    A = ord('A')
    a = ord('a')
    zero = ord('0')
    one = ord('1')

    def elem():
        nonlocal state
        state, du = draw_hi(state)
        buf.append(A + du % 6)
        if (du // 6) % 2 == 0:
            state, dl = draw_hi(state)
            buf.append(a + dl % 3)
        state, dc = draw_hi(state)
        buf.append(one + dc % 9)
        dpos.append(len(buf) - 1)

    def mult():
        nonlocal state
        state, dm = draw_hi(state)
        buf.append(zero + 2 + dm % 8)
        dpos.append(len(buf) - 1)

    for _ in range(num_chunks):
        state, r = draw_hi(state)
        tt = r % 5
        if tt == 0:
            elem()
        elif tt == 1:
            elem()
            elem()
        elif tt == 2:
            buf.append(ord('('))
            elem()
            elem()
            buf.append(ord(')'))
            mult()
        elif tt == 3:
            buf.append(ord('('))
            elem()
            buf.append(ord('('))
            elem()
            elem()
            buf.append(ord(')'))
            mult()
            buf.append(ord(')'))
            mult()
        else:
            buf.append(ord('('))
            elem()
            elem()
            elem()
            buf.append(ord(')'))
            mult()

    n = len(buf)
    ndig = len(dpos)
    LP = ord('(')
    RP = ord(')')

    sink = 0
    for p in range(passes):
        pos = dpos[p % ndig]
        buf[pos] = one + ((buf[pos] - one + 1) % 9)

        nid = []
        counts = []
        pst = []

        i = 0
        while i < n:
            b = buf[i]
            if b == LP:
                pst.append(len(nid))
                i += 1
            elif b == RP:
                i += 1
                m = 0
                have = False
                while i < n and is_digit(buf[i]):
                    m = m * 10 + (buf[i] - zero)
                    have = True
                    i += 1
                if not have:
                    m = 1
                start = pst.pop()
                for k in range(start, len(nid)):
                    counts[k] *= m
            elif is_upper(b):
                up = b - A
                i += 1
                low = 0
                if i < n and is_lower(buf[i]):
                    low = (buf[i] - a) + 1
                    i += 1
                idv = up * 4 + low
                c = 0
                have2 = False
                while i < n and is_digit(buf[i]):
                    c = c * 10 + (buf[i] - zero)
                    have2 = True
                    i += 1
                if not have2:
                    c = 1
                nid.append(idv)
                counts.append(c)
            else:
                i += 1

        mapc = {}
        for e in range(len(nid)):
            k = nid[e]
            mapc[k] = mapc.get(k, 0) + counts[e]

        checksum = 0
        for id2 in range(id_range):
            checksum += id2 * mapc.get(id2, 0)
        sink += checksum

    print(sink)


main()
