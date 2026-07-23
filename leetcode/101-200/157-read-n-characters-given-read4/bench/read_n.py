"""Benchmark workload for LeetCode #157 — Read N Characters Given Read4
(Python; scale lane)."""


class Reader:
    __slots__ = ("pos", "chk")

    def __init__(self):
        self.pos = 0
        self.chk = 0


def read4(src, m, rd):
    cnt = 0
    while cnt < 4 and rd.pos < m:
        rd.pos += 1
        cnt += 1
    return cnt


def read_n(src, m, rd, want):
    total = 0
    acc = rd.chk
    eof = False
    while total < want and not eof:
        start = rd.pos
        cnt = read4(src, m, rd)
        if cnt == 0:
            eof = True
        else:
            take = cnt if total + cnt <= want else want - total
            for k in range(take):
                acc = (acc * 1103515245 + src[start + k] + 1) & 2147483647
            total += take
    rd.chk = acc
    return total


def main():
    size = 50000
    want = 7
    passes = 3200

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
        cont = True
        while cont:
            got = read_n(src, size, rd, want)
            if got == 0:
                cont = False
    print(rd.chk)


main()
