"""Benchmark workload for LeetCode #146 — LRU Cache (Python; scale lane)."""


def main():
    cap = 1024
    key_range = 4096
    ops = 32000000

    pool = cap + 2
    nkey = [-1] * pool
    nval = [0] * pool
    nprev = [-1] * pool
    nnext = [-1] * pool
    nnext[0] = 1
    nprev[1] = 0

    m = {}
    size = 0
    sink = 0
    state = 12345

    for _ in range(ops):
        state = (state * 1103515245 + 12345) & 2147483647
        h1 = state >> 16
        state = (state * 1103515245 + 12345) & 2147483647
        h2 = state >> 16
        key = h2 % key_range

        if h1 % 2 == 0:
            idx = m.get(key, -1)
            r = -1
            if idx >= 0:
                pi = nprev[idx]
                ni = nnext[idx]
                nnext[pi] = ni
                nprev[ni] = pi
                first = nnext[0]
                nprev[idx] = 0
                nnext[idx] = first
                nprev[first] = idx
                nnext[0] = idx
                r = nval[idx]
            sink += r + 1
        else:
            state = (state * 1103515245 + 12345) & 2147483647
            v = state >> 16
            existing = m.get(key, -1)
            if existing >= 0:
                nval[existing] = v
                pi = nprev[existing]
                ni = nnext[existing]
                nnext[pi] = ni
                nprev[ni] = pi
                first = nnext[0]
                nprev[existing] = 0
                nnext[existing] = first
                nprev[first] = existing
                nnext[0] = existing
            else:
                if size < cap:
                    idx = 2 + size
                    size += 1
                else:
                    lru = nprev[1]
                    pl = nprev[lru]
                    nl = nnext[lru]
                    nnext[pl] = nl
                    nprev[nl] = pl
                    del m[nkey[lru]]
                    idx = lru
                nkey[idx] = key
                nval[idx] = v
                m[key] = idx
                first = nnext[0]
                nprev[idx] = 0
                nnext[idx] = first
                nprev[first] = idx
                nnext[0] = idx

    print(sink)


main()
