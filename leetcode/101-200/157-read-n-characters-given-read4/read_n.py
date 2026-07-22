"""LeetCode 157 — Read N Characters Given Read4 (Python mirror / oracle). Premium.

read4 returns up to 4 chars from the source cursor; read(n) pulls chunks until n
chars are collected or EOF, taking only as many as still needed from the last
chunk. Mirrors the Kāra version.
"""


class Reader:
    def __init__(self, src):
        self.src = src
        self.pos = 0

    def read4(self):
        chunk = self.src[self.pos:self.pos + 4]
        self.pos += len(chunk)
        return chunk


def read(rd, n):
    result = []
    total = 0
    while total < n:
        chunk = rd.read4()
        if not chunk:
            break
        take = len(chunk) if total + len(chunk) <= n else n - total
        result.append(chunk[:take])
        total += take
    return "".join(result)


def run(src, n):
    rd = Reader(src)
    r = read(rd, n)
    print(f"{len(r)} {r}")


def main():
    run("abc", 4)
    run("HelloWorld", 5)
    run("HelloWorld", 12)
    run("", 3)
    run("read4test", 7)


main()
