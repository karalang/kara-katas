"""LeetCode #135: Candy — two greedy passes."""


def candy(ratings):
    n = len(ratings)
    if n == 0:
        return 0
    c = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            c[i] = c[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1] and c[i] <= c[i + 1]:
            c[i] = c[i + 1] + 1
    return sum(c)


def lcg(seed, n, mod):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(x % mod)
    return out


def main():
    MOD = 1000000007
    sink = 0
    cases = [[1, 0, 2], [1, 2, 2], [1, 3, 2, 2, 1], [5, 4, 3, 2, 1], [1, 2, 3, 4, 5]]
    for t in range(6):
        cases.append(lcg(t + 1, 12 + t * 4, 5))
    for r in cases:
        v = candy(r)
        print(f"n={len(r)}: {v}")
        sink = (sink * 1000003 + v) % MOD
    print(f"sink: {sink}")


if __name__ == "__main__":
    main()
