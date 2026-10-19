# LeetCode 774 — Minimize Max Distance to Gas Station: the ★ arm and
# harness in Python.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(stations, k):
    print(f"{stations}, k = {k} -> {minmax_gas_dist(stations, k):.5f}")


def main():
    global seed
    show([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9)
    show([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1)
    show([0, 100], 3)
    show([0, 10, 20], 1)
    show([0, 1], 31)
    show([0, 1], 63)
    show([0, 7, 100000000], 1000000)
    show([0, 3, 4, 10, 11, 20], 5)
    seed = 774
    total = 0.0
    check = 0
    for _ in range(300):
        n = 10 + next_random() % 51
        spread = 1000000 if next_random() % 4 == 0 else 1000
        stations = [next_random() % 100]
        for _ in range(1, n):
            stations.append(stations[-1] + 1 + next_random() % spread)
        k = 1 + next_random() % 2000
        answer = minmax_gas_dist(stations, k)
        total += answer
        check = (check * 31 + int(answer * 1000000.0)) % 1000000007
    print(f"300 random cases: answers sum to {total:.5f}, checksum {check}")


main()
