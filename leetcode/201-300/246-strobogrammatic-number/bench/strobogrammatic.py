"""Benchmark mirror for LeetCode #246 - Strobogrammatic Number.

Build-once + punch (BENCHMARKS.md): 20,000 length-32 numbers are built ONCE,
then 100 passes run the two-pointer check over all of them - 2,000,000 calls.

The corpus is deliberately mostly ACCEPTING. A uniform digit draw would make
almost every number reject on its first character, and the benchmark would then
measure loop entry and early return rather than the scan it claims to measure.
So every number is constructed strobogrammatic, and 1 in 8 is corrupted at one
random position - which rejects, but on average halfway through, so a reject
still does real work.

Timed separately from the compiled lanes - see BENCHMARKS.md.
"""

N = 20000
LEN = 32
PASSES = 100

ROT = {"0": "0", "1": "1", "8": "8", "6": "9", "9": "6"}
PAIRS = [("0", "0"), ("1", "1"), ("8", "8"), ("6", "9"), ("9", "6")]
ALL = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def lcg(state):
    return (state * 1103515245 + 12345) & 2147483647


def is_strobogrammatic(num):
    lo = 0
    hi = len(num) - 1
    while lo <= hi:
        a = num[lo]
        if a not in ROT or ROT[a] != num[hi]:
            return False
        lo += 1
        hi -= 1
    return True


def main():
    state = 1
    corpus = []
    for _ in range(N):
        chars = [""] * LEN
        lo, hi = 0, LEN - 1
        while lo < hi:
            state = lcg(state)
            a, b = PAIRS[(state // 65536) % 5]
            chars[lo], chars[hi] = a, b
            lo += 1
            hi -= 1
        state = lcg(state)
        if (state // 65536) % 8 == 0:
            state = lcg(state)
            pos = (state // 65536) % LEN
            state = lcg(state)
            chars[pos] = ALL[(state // 65536) % 10]
        corpus.append("".join(chars))

    acc = 0
    for _ in range(PASSES):
        for num in corpus:
            acc = (acc * 131 + (1 if is_strobogrammatic(num) else 0)) % 1000000007
    print(acc)


main()
