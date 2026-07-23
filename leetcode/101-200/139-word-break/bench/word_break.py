"""Build-once + punch word-break (LeetCode #139; Python scale lane).

The dictionary is a SET realized as a flat stamped bytearray table keyed by a
per-length base-A word encoding (mirrors the Set[String] kata; see
word_break.kara)."""


def main():
    alpha = 5
    maxlen = 4
    n = 5000
    dwords = 120
    win = 24
    windows = 2200000

    base = [0, 0]
    pwr = alpha
    acc = 0
    b = 2
    while b <= maxlen:
        acc += pwr
        base.append(acc)
        pwr *= alpha
        b += 1
    tsize = acc + pwr

    table = bytearray(tsize)

    state = 12345

    s = [0] * n
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        r = state >> 16
        s[i] = r % alpha

    for _ in range(dwords):
        state = (state * 1103515245 + 12345) & 2147483647
        rl = state >> 16
        wlen = 2 + (rl % (maxlen - 1))
        code = 0
        for _ in range(wlen):
            state = (state * 1103515245 + 12345) & 2147483647
            rc = state >> 16
            code = code * alpha + (rc % alpha)
        table[base[wlen] + code] = 1

    dp = bytearray(win + 1)

    sink = 0
    for _ in range(windows):
        state = (state * 1103515245 + 12345) & 2147483647
        ro = state >> 16
        off = ro % (n - win)

        for z in range(win + 1):
            dp[z] = 0
        dp[0] = 1

        ii = 1
        while ii <= win:
            low = ii - maxlen if ii > maxlen else 0
            code = 0
            pw = 1
            ln = 0
            j = ii - 1
            while j >= low:
                ch = s[off + j]
                code = ch * pw + code
                pw *= alpha
                ln += 1
                if dp[j]:
                    if table[base[ln] + code]:
                        dp[ii] = 1
                        break
                j -= 1
            ii += 1

        if dp[win]:
            sink += off + 1

    print(sink)


main()
