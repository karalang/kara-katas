MOD = 1000000007


def num_of_arrays(n, m, k):
    ways = [[0] * (k + 1) for _ in range(m + 1)]
    if k >= 1:
        for j in range(1, m + 1):
            ways[j][1] = 1
    for _ in range(1, n):
        nxt = [[0] * (k + 1) for _ in range(m + 1)]
        for c in range(1, k + 1):
            below = 0
            for j in range(1, m + 1):
                nxt[j][c] = (ways[j][c] * j + below) % MOD
                below = (below + ways[j][c - 1]) % MOD
        ways = nxt
    total = 0
    for j in range(1, m + 1):
        total = (total + ways[j][k]) % MOD
    return total


def main():
    seed = 1420
    check = 0
    for _ in range(1000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = seed // 65536 % 51
        check = (check * 131 + num_of_arrays(50, 100, k)) % 1000000007
    print(f"1000 values of k at n = 50, m = 100: checksum {check}")


main()
