"""Benchmark harness for LeetCode #134 — Gas Station.

Mirrors gas_station.kara algorithm-for-algorithm. Committed as the correctness
oracle; not a measured lane.
"""

NP = 8
N = 200000
ITERS = 1200


def can_complete(gas, cost):
    n = len(gas)
    total = 0
    tank = 0
    start = 0
    for i in range(n):
        d = gas[i] - cost[i]
        total += d
        tank += d
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1


def lcg(seed, n, cap):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x // 65536) % cap)
    return out


def main():
    gases = []
    costs = []
    for j in range(NP):
        gases.append(lcg(j + 1, N, 100))
        costs.append(lcg(j + 100, N, 90 if j % 2 == 0 else 110))

    sink = 0
    for it in range(ITERS):
        idx = (it * 3) % NP
        sink = (sink + can_complete(gases[idx], costs[idx])) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
