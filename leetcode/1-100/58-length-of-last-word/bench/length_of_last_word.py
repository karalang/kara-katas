"""Benchmark workload for LeetCode #58 — Length of Last Word (Python; scale lane)."""


def last_word_len(buf, end):
    i = end
    while i >= 0 and buf[i] == 32:
        i -= 1
    length = 0
    while i >= 0 and buf[i] != 32:
        length += 1
        i -= 1
    return length


def main():
    n = 4000000
    passes = 6500000
    buf = []
    state = 12345
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        r = state >> 16
        if r % 100 < 18:
            buf.append(32)
        else:
            buf.append(65 + r % 26)

    sink = 0
    for p in range(passes):
        idx = (p * 97 + 13) % n
        if buf[idx] == 32:
            buf[idx] = 65 + p % 26
        else:
            buf[idx] = 32
        e = (p * 89 + 41) % n
        sink += last_word_len(buf, e)
    print(sink)


main()
