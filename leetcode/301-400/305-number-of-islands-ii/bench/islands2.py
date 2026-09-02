# Benchmark mirror — LeetCode 305, Number of Islands II.
# Same algorithm, same Fisher-Yates over the same LCG, same masked sink as
# islands2.kara. See ../README.md § Benchmarks.
#
# The sink masks rather than taking a modulus: Python's `%` FLOORS while
# C/Rust/Go/kara truncate toward zero, so a modulo sink over a signed running
# total prints a different number here than in every other mirror (measured on
# #303). Masking is two's-complement in all five languages.


def main():
    n = 256
    cells = n * n
    passes = 160

    order = list(range(cells))
    state = 20305
    i = cells - 1
    while i > 0:
        state = (state * 1103515245 + 12345) % 2147483648
        j = state % (i + 1)
        order[i], order[j] = order[j], order[i]
        i -= 1

    checksum = 0
    for _ in range(passes):
        parent = [-1] * cells
        rank = [0] * cells
        count = 0
        for idx in order:
            r = idx // n
            c = idx % n
            parent[idx] = idx
            count += 1
            for d in range(4):
                nb = -1
                if d == 0 and r > 0:
                    nb = idx - n
                elif d == 1 and r < n - 1:
                    nb = idx + n
                elif d == 2 and c > 0:
                    nb = idx - 1
                elif d == 3 and c < n - 1:
                    nb = idx + 1
                if nb >= 0 and parent[nb] >= 0:
                    ra = idx
                    while parent[ra] != ra:
                        ra = parent[ra]
                    cur = idx
                    while parent[cur] != ra:
                        nx = parent[cur]
                        parent[cur] = ra
                        cur = nx
                    rb = nb
                    while parent[rb] != rb:
                        rb = parent[rb]
                    cur = nb
                    while parent[cur] != rb:
                        nx = parent[cur]
                        parent[cur] = rb
                        cur = nx
                    if ra != rb:
                        if rank[ra] < rank[rb]:
                            parent[ra] = rb
                        elif rank[ra] > rank[rb]:
                            parent[rb] = ra
                        else:
                            parent[rb] = ra
                            rank[ra] += 1
                        count -= 1
            checksum = (checksum + count) & 0x3FFFFFFF
    print(f"checksum {checksum}")


main()
