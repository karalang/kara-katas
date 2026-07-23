"""Build-once + punch reorder-list over an index pool (LeetCode #143; Python
scale lane). Each pass generates the interleaved order, rewires nxt, and walks
it, folding a position-weighted checksum into the sink (see reorder_list.kara)."""


def main():
    n = 100000
    k = 1000
    valmod = 1000

    vals = [0] * n
    nxt = [0] * n
    order = [0] * n

    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        vals[i] = (state >> 16) % valmod

    sink = 0
    for p in range(k):
        pi = p % n
        vals[pi] = (vals[pi] + 1) % valmod

        lo = 0
        hi = n - 1
        idx = 0
        take_lo = True
        while lo <= hi:
            if take_lo:
                order[idx] = lo
                lo += 1
            else:
                order[idx] = hi
                hi -= 1
            take_lo = not take_lo
            idx += 1

        r = 0
        while r + 1 < n:
            nxt[order[r]] = order[r + 1]
            r += 1
        nxt[order[n - 1]] = -1

        cur = order[0]
        pos = 0
        while cur >= 0:
            w = (pos % 997) + 1
            sink += w * vals[cur]
            pos += 1
            cur = nxt[cur]

    print(sink)


main()
