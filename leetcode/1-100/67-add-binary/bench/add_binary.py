"""Benchmark workload for LeetCode #67 — Add Binary (Python; scale lane)."""

W = 96


def add_popcount(bits, off_a, off_b):
    carry = 0
    pop = 0
    k = W - 1
    while k >= 0:
        s = carry + bits[off_a + k] + bits[off_b + k]
        pop += s & 1
        carry = s >> 1
        k -= 1
    pop += carry
    return pop


def main():
    bn = 2000000
    passes = 2600000
    bits = []
    state = 12345
    for _ in range(bn):
        state = (state * 1103515245 + 12345) & 2147483647
        bits.append((state >> 16) & 1)

    span = bn - W
    sink = 0
    for p in range(passes):
        idx = (p * 101 + 7) % bn
        bits[idx] = 1 - bits[idx]
        off_a = (p * 37) % span
        off_b = (p * 53 + 17) % span
        sink += add_popcount(bits, off_a, off_b)
    print(sink)


main()
