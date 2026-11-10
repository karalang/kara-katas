# LeetCode #2064: Minimized Maximum of Products Distributed to Any Store --
# Python mirror of the ★ arm's benchmark (stores.kara): 200 problems of
# 50000 types, quantities from 1 to 100000, and from 50000 to 100000 stores.


def minimized_maximum(n, quantities):
    lo, hi = 1, max(quantities)
    while lo < hi:
        mid = (lo + hi) // 2
        need = 0
        for q in quantities:
            need += (q + mid - 1) // mid
        if need <= n:
            hi = mid
        else:
            lo = mid + 1
    return lo


seed = 2064


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    total = 0
    check = 0
    for _ in range(200):
        qs = [(next_random() * 32768 + next_random()) % 100000 + 1 for _ in range(50000)]
        n = 50000 + (next_random() * 32768 + next_random()) % 50001
        a = minimized_maximum(n, qs)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"200 problems: sum {total}, checksum {check}")


main()
