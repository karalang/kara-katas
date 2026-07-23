"""Benchmark workload for LeetCode #205 — Isomorphic Strings (Python; scale lane)."""


def main():
    length = 600000
    w = 200
    a = 20011
    s = [0] * length
    t = [0] * length
    state = 12345
    for i in range(length):
        state = (state * 1103515245 + 12345) & 2147483647
        s[i] = state % a
    for i in range(length):
        state = (state * 1103515245 + 12345) & 2147483647
        t[i] = state % a

    st_val = [0] * a
    st_ver = [-1] * a
    ts_val = [0] * a
    ts_ver = [-1] * a

    sink = 0
    last = length - w + 1
    for start in range(last):
        stamp = start
        iso = True
        k = 0
        while iso and k < w:
            ch = s[start + k]
            dh = t[start + k]
            if st_ver[ch] != stamp:
                st_ver[ch] = stamp
                st_val[ch] = dh
            elif st_val[ch] != dh:
                iso = False
            if iso:
                if ts_ver[dh] != stamp:
                    ts_ver[dh] = stamp
                    ts_val[dh] = ch
                elif ts_val[dh] != ch:
                    iso = False
            k += 1
        if iso:
            sink += 1
    print(sink)


main()
