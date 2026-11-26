# LeetCode #1420, Python mirror of num_of_arrays.kara: ways[j][c], the
# arrays so far whose largest is j and whose search cost is c; one element
# more is at most the largest, j ways, or a new largest, which costs one
# search more.

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
    return sum(ways[j][k] for j in range(1, m + 1)) % MOD


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    cases = [(2, 3, 1), (5, 2, 3), (9, 1, 1), (1, 1, 1), (1, 5, 0), (3, 3, 3), (4, 2, 2), (50, 100, 25)]
    print(" ".join(str(num_of_arrays(n, m, k)) for n, m, k in cases))
    print(f"n = 50, m = 100: {num_of_arrays(50, 100, 1)} {num_of_arrays(50, 100, 2)} {num_of_arrays(50, 100, 50)}")
    seed = 1420
    check = 0
    zero = 0
    for _ in range(2000):
        n = 1 + next_random() % 12
        m = 1 + next_random() % 30
        k = next_random() % (n + 1)
        got = num_of_arrays(n, m, k)
        if got == 0:
            zero += 1
        check = (check * 131 + got) % 1000000007
    print(f"2000 random cases: {zero} with no array, checksum {check}")


main()
