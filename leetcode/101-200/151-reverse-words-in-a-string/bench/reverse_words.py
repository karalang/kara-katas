"""Benchmark workload for LeetCode #151 — Reverse Words in a String (Python; scale lane)."""


def main():
    length = 200000
    passes = 320
    modp = 1000000007
    space = 32

    buf = [0] * length
    ws = [0] * length
    we = [0] * length
    state = 12345
    for i in range(length):
        state = (state * 1103515245 + 12345) & 2147483647
        if state % 100 < 15:
            buf[i] = space
        else:
            buf[i] = 97 + state % 26

    sink = 0
    for _p in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        idx = state % length
        state = (state * 1103515245 + 12345) & 2147483647
        if state % 100 < 15:
            buf[idx] = space
        else:
            buf[idx] = 97 + state % 26

        i = 0
        m = 0
        while i < length:
            while i < length and buf[i] == space:
                i += 1
            if i >= length:
                break
            start = i
            while i < length and buf[i] != space:
                i += 1
            ws[m] = start
            we[m] = i
            m += 1

        k = m - 1
        while k >= 0:
            if k < m - 1:
                sink = (sink * 131 + space) % modp
            e = we[k]
            j = ws[k]
            while j < e:
                sink = (sink * 131 + buf[j]) % modp
                j += 1
            k -= 1
    print(sink)


main()
