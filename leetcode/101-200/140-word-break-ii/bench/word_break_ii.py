"""Exponential-backtracking segmentation COUNT for LeetCode #140 (Python scale
lane). Short strings / small dicts keep the search tractable; counts are bounded
by compositions of SLEN so the sink never overflows. Dict SET is a flat stamped
base-A bytearray table (see word_break_ii.kara)."""

ALPHA = 3
MINLEN = 1
MAXLEN = 3
SLEN = 16


def main():
    dwords = 25
    cases = 80000

    base = [0, 0]
    pwr = ALPHA
    acc = 0
    b = 2
    while b <= MAXLEN:
        acc += pwr
        base.append(acc)
        pwr *= ALPHA
        b += 1
    tsize = acc + pwr

    table = bytearray(tsize)
    s = [0] * SLEN

    def count(start):
        if start == SLEN:
            return 1
        total = 0
        code = 0
        end = start + 1
        while end <= SLEN and end - start <= MAXLEN:
            code = code * ALPHA + s[end - 1]
            ln = end - start
            if ln >= MINLEN:
                if table[base[ln] + code]:
                    total += count(end)
            end += 1
        return total

    state = 12345
    sink = 0

    for _ in range(cases):
        for z in range(tsize):
            table[z] = 0
        for i in range(SLEN):
            state = (state * 1103515245 + 12345) & 2147483647
            r = state >> 16
            s[i] = r % ALPHA
        for _ in range(dwords):
            state = (state * 1103515245 + 12345) & 2147483647
            rl = state >> 16
            span = MAXLEN - MINLEN + 1
            wlen = MINLEN + (rl % span)
            code = 0
            for _ in range(wlen):
                state = (state * 1103515245 + 12345) & 2147483647
                rc = state >> 16
                code = code * ALPHA + (rc % ALPHA)
            table[base[wlen] + code] = 1

        sink += count(0)

    print(sink)


main()
