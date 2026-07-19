"""LeetCode #134: Gas Station — greedy single pass.

If total(gas) >= total(cost) a unique start exists: track a running tank; when it
goes negative, no station up to here can be the start, so restart from the next.
Return that start index, or -1.
"""


def can_complete(gas, cost):
    total = 0
    tank = 0
    start = 0
    for i in range(len(gas)):
        d = gas[i] - cost[i]
        total += d
        tank += d
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1


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
    cases = [
        ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]),   # 3
        ([2, 3, 4], [3, 4, 3]),               # -1
        ([5], [4]),                           # 0
        ([3, 3, 4], [3, 4, 4]),               # -1
    ]
    for t in range(6):
        n = 8 + t * 3
        gas = lcg(t + 1, n, 20)
        cost = lcg(t + 100, n, 20)
        cases.append((gas, cost))
    for gas, cost in cases:
        r = can_complete(gas, cost)
        print(f"n={len(gas)}: {r}")
        sink = (sink * 1000003 + (r + 2)) % MOD
    print(f"sink: {sink}")


if __name__ == "__main__":
    main()
