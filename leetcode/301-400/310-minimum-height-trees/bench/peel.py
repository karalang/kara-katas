# Benchmark mirror — LeetCode 310, Minimum Height Trees.
# Same four CSR trees, same LCG, same leaf-peeling, same checksum-driven tree
# selection and masked sink as peel.kara. See ../README.md § Benchmarks.
#
# The sink masks rather than taking a modulus: Python's `%` FLOORS while
# C/Rust/Go/kara truncate toward zero (measured on #303). Masking is
# two's-complement in all five languages.


def main():
    n = 60000
    trees = 4
    passes = 950

    all_off = []
    all_nbr = []
    state = 20310
    deg = [0] * n
    pa = [0] * n
    cursor = [0] * n

    for t in range(trees):
        window = 1 + t * 3
        for i in range(n):
            deg[i] = 0
        pa[0] = 0
        for i in range(1, n):
            w = window if window <= i else i
            state = (state * 1103515245 + 12345) % 2147483648
            p = i - 1 - state % w
            pa[i] = p
            deg[i] += 1
            deg[p] += 1
        base = len(all_off)
        running = len(all_nbr)
        for k in range(n):
            all_off.append(running)
            running += deg[k]
        all_off.append(running)
        for k in range(n):
            cursor[k] = all_off[base + k]
        while len(all_nbr) < running:
            all_nbr.append(0)
        for i in range(1, n):
            p = pa[i]
            all_nbr[cursor[i]] = p
            cursor[i] += 1
            all_nbr[cursor[p]] = i
            cursor[p] += 1

    checksum = 0
    degree = [0] * n
    alive = [0] * n
    layer = [0] * n
    nxt = [0] * n

    for p in range(passes):
        which = (p + checksum) % trees
        base = which * (n + 1)

        lcount = 0
        for i in range(n):
            d = all_off[base + i + 1] - all_off[base + i]
            degree[i] = d
            alive[i] = 1
            if d == 1:
                layer[lcount] = i
                lcount += 1

        remaining = n
        while remaining > 2:
            remaining -= lcount
            ncount = 0
            for k in range(lcount):
                v = layer[k]
                alive[v] = 0
                for j in range(all_off[base + v], all_off[base + v + 1]):
                    w = all_nbr[j]
                    if alive[w] == 1:
                        degree[w] -= 1
                        if degree[w] == 1:
                            nxt[ncount] = w
                            ncount += 1
            for c in range(ncount):
                layer[c] = nxt[c]
            lcount = ncount

        acc = 0
        for i in range(n):
            if alive[i] == 1:
                acc += i
        checksum = (checksum + acc) & 0x3FFFFFFF
    print(f"checksum {checksum}")


main()
