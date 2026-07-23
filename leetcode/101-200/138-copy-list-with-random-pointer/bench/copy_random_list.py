"""Benchmark workload for LeetCode #138 — Copy List with Random Pointer (Python; scale lane)."""


def main():
    n = 3000
    k = 40000

    oval = [0] * n
    onext = [0] * n
    ornd = [0] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        oval[i] = (state >> 16) % 1000
        onext[i] = i + 1 if i + 1 < n else -1
        state = (state * 1103515245 + 12345) & 2147483647
        r = state >> 16
        ornd[i] = -1 if r % 4 == 0 else r % n

    map_ = [0] * n
    nval = [0] * n
    nnext = [0] * n
    nrnd = [0] * n

    sink = 0
    for p in range(k):
        ii = p % n
        ornd[ii] = (p * 37 + 11) % n

        for i in range(n):
            nval[i] = oval[i]
            map_[i] = i
        for i in range(n):
            nnext[i] = -1 if onext[i] == -1 else map_[onext[i]]
            nrnd[i] = -1 if ornd[i] == -1 else map_[ornd[i]]
        checksum = 0
        for i in range(n):
            checksum += nval[i] + nnext[i] * 7 + nrnd[i] * 13
        sink += checksum
    print(sink)


main()
