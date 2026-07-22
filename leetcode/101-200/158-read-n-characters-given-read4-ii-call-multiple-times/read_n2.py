"""LeetCode 158 — Read4 II, call multiple times (Python mirror / oracle). Premium.

read(n) called repeatedly; leftover chars from read4 persist in the Reader's
buffer between calls. Mirrors the Kāra version.
"""


class Reader:
    def __init__(self, src):
        self.src = src
        self.pos = 0
        self.buf = ""
        self.buf_pos = 0

    def read4(self):
        chunk = self.src[self.pos:self.pos + 4]
        self.pos += len(chunk)
        return chunk

    def read(self, n):
        result = []
        total = 0
        while total < n:
            if self.buf_pos >= len(self.buf):
                self.buf = self.read4()
                self.buf_pos = 0
                if len(self.buf) == 0:
                    return "".join(result)
            result.append(self.buf[self.buf_pos])
            self.buf_pos += 1
            total += 1
        return "".join(result)


def main():
    rd = Reader("HelloWorld")
    print(rd.read(2))
    print(rd.read(3))
    print(rd.read(10))
    print(rd.read(1))

    r2 = Reader("abcdefghij")
    print(r2.read(1))
    print(r2.read(5))
    print(r2.read(100))


main()
