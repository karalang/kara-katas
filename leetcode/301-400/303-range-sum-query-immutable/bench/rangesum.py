"""Benchmark mirror of rangesum.kara - LeetCode #303, O(1) prefix-sum query.

Same LCG, same query list, same sink.

The sink is a mask rather than a modulo, and the kara lane's header explains
why: a mod-p sink cost more than the query it was supposed to be measuring and
made every compiled language tie. `&` on a negative left operand agrees across
all five languages (Python's arbitrary-precision ints use two's-complement
semantics for bitwise ops), so no correction idiom is needed here - unlike `%`,
which truncates toward zero in kara/C/Rust/Go and floors in Python.
"""

N = 65536
NQUERIES = 200000
PASSES = 1800


def main() -> None:
    state = 20303

    prefix = [0] * (N + 1)
    for i in range(N):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        v = (state // 65536) % 2001 - 1000
        prefix[i + 1] = prefix[i] + v

    qs = [0] * (NQUERIES * 2)
    for q in range(NQUERIES):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        x = (state // 65536) % N
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        y = (state // 65536) % N
        if x <= y:
            qs[q * 2], qs[q * 2 + 1] = x, y
        else:
            qs[q * 2], qs[q * 2 + 1] = y, x

    checksum = 0
    for _ in range(PASSES):
        for k in range(NQUERIES):
            v = prefix[qs[k * 2 + 1] + 1] - prefix[qs[k * 2]]
            checksum = (checksum + v) & 0x3FFFFFFF

    print(f"checksum {checksum}")


if __name__ == "__main__":
    main()
