"""Benchmark harness for LeetCode #242 — Valid Anagram.

Mirrors valid_anagram.kara algorithm-for-algorithm, including the explicit
26-slot frequency array rather than collections.Counter, so the measured work
matches.
"""

NP = 8
SL = 20000
ITERS = 8000


def is_anagram(s, t):
    if len(s) != len(t):
        return False
    count = [0] * 26
    for i in range(len(s)):
        count[s[i] - 97] += 1
        count[t[i] - 97] -= 1
    for j in range(26):
        if count[j] != 0:
            return False
    return True


def main():
    esses = []
    tees = []
    for j in range(NP):
        sj = bytearray(97 + ((k * 7 + j) % 26) for k in range(SL))
        tj = bytearray()
        for m in range(SL - 1, -1, -1):
            b = sj[m]
            if j % 2 == 1 and m == 0:
                b = 97 + ((b - 97 + 1) % 26)
            tj.append(b)
        esses.append(sj)
        tees.append(tj)

    sink = 0
    for it in range(ITERS):
        idx = (it * 3) % NP
        if is_anagram(esses[idx], tees[idx]):
            sink += it + 1
        else:
            sink += 1
    print(sink)


if __name__ == "__main__":
    main()
