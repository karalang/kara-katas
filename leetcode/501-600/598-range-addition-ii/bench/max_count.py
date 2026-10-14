# Benchmark for #598: Python mirror of the ★ arm (the smallest corner);
# see max_count.kara.


def max_count(m, n, ops):
    rows = m
    cols = n
    for op in ops:
        rows = min(rows, op[0])
        cols = min(cols, op[1])
    return rows * cols


# ---- benchmark ---------------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def wide(seed):
    hi = step(seed)
    lo = step(seed)
    return hi * 32768 + lo


def main():
    count = 100
    rounds = 300
    seed = [598]
    sizes = []
    lists = []
    for _ in range(count):
        m = 1 + wide(seed) % 40000
        n = 1 + wide(seed) % 40000
        ops = []
        for _ in range(10000):
            a = m - step(seed) % (1 + m // 8)
            b = n - step(seed) % (1 + n // 8)
            ops.append([a, b])
        sizes.append((m, n))
        lists.append(ops)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            c = (rnd * 7 + g) % count
            m, n = sizes[c]
            got = max_count(m, n, lists[c])
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} lists, {rounds} rounds: total {total}, checksum {checksum}")


main()
