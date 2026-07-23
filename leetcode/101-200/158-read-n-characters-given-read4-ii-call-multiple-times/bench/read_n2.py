"""Benchmark workload for LeetCode #158 — Read N Characters Given Read4 II
(call multiple times) (Python; scale lane)."""


class Reader:
    __slots__ = ("pos", "chk", "buf_start", "buf_len", "buf_pos")

    def __init__(self):
        self.pos = 0
        self.chk = 0
        self.buf_start = 0
        self.buf_len = 0
        self.buf_pos = 0


def read4(src, m, rd):
    rd.buf_start = rd.pos
    cnt = 0
    while cnt < 4 and rd.pos < m:
        rd.pos += 1
        cnt += 1
    rd.buf_len = cnt
    rd.buf_pos = 0
    return cnt


def read_n(src, m, rd, want):
    total = 0
    acc = rd.chk
    eof = False
    while total < want and not eof:
        if rd.buf_pos >= rd.buf_len:
            cnt = read4(src, m, rd)
            if cnt == 0:
                eof = True
        if not eof:
            c = src[rd.buf_start + rd.buf_pos]
            acc = (acc * 1103515245 + c + 1) & 2147483647
            rd.buf_pos += 1
            total += 1
    rd.chk = acc
    return total


def main():
    size = 50000
    want = 3
    passes = 2600

    src = [0] * size
    state = 12345
    for c in range(size):
        state = (state * 1103515245 + 12345) & 2147483647
        src[c] = state % 26

    rd = Reader()
    for p in range(passes):
        idx = (p * 131 + 7) % size
        src[idx] = (src[idx] + 1) % 26
        rd.pos = 0
        rd.buf_len = 0
        rd.buf_pos = 0
        rd.buf_start = 0
        cont = True
        while cont:
            got = read_n(src, size, rd, want)
            if got == 0:
                cont = False
    print(rd.chk)


main()
