# Benchmark for #667: zigzag from both ends, as the Kara ★ arm.


def construct_array(n, k):
    out = []
    lo, hi = 1, k + 1
    while lo <= hi:
        out.append(lo)
        lo += 1
        if lo <= hi:
            out.append(hi)
            hi -= 1
    for x in range(k + 2, n + 1):
        out.append(x)
    return out


def main():
    n = 10000
    rounds = 10000
    s = 0
    for r in range(rounds):
        k = 1 + r * 7919 % (n - 1)
        for x in construct_array(n, k):
            s = (s * 31 + x) % 1000000007
    print(f"n = {n}, {rounds} rounds: checksum {s}")


main()
