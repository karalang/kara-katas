# LeetCode 774 — Minimize Max Distance to Gas Station: benchmark, the ★
# arm in Python. Sixty-four random roads of 2,000 stations, LeetCode's
# limit, spread over up to 10^8, each with k from 1 to 10^6, built once;
# ROUNDS rounds each solve the next of them.

ROUNDS = 2000


def minmax_gas_dist(stations, k):
    lo = 0.0
    hi = 0.0
    for i in range(1, len(stations)):
        gap = float(stations[i] - stations[i - 1])
        if gap > hi:
            hi = gap
    hi += 1.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        needed = 0
        for i in range(1, len(stations)):
            needed += int(float(stations[i] - stations[i - 1]) / mid)
        if needed <= k:
            hi = mid
        else:
            lo = mid
    longest = 0.0
    for i in range(1, len(stations)):
        gap = float(stations[i] - stations[i - 1])
        piece = gap / float(int(gap / hi) + 1)
        if piece > longest:
            longest = piece
    return longest


seed = 774


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    roads = []
    ks = []
    for _ in range(64):
        stations = [next_random() % 100]
        for _ in range(1, 2000):
            stations.append(stations[-1] + 1 + (next_random() * 32768 + next_random()) % 50000)
        roads.append(stations)
        ks.append(1 + (next_random() * 32768 + next_random()) % 1000000)
    total = 0.0
    for r in range(ROUNDS):
        total += minmax_gas_dist(roads[r % 64], ks[r % 64])
    print(f"{ROUNDS} roads of 2000 stations: answers sum to {total:.5f}")


main()
