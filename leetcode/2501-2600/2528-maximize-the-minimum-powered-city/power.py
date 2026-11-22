# LeetCode #2528: Maximize the Minimum Powered City -- Python mirror of
# the ★ arm (power.kara): powers from prefix sums, then a binary search on
# the answer with a greedy sweep that places each shortfall as far right
# as still reaches the city.


def reachable(power, r, k, target):
    n = len(power)
    ends = [0] * (n + 1)
    running = 0
    used = 0
    for i in range(n):
        running += ends[i]
        have = power[i] + running
        if have < target:
            need = target - have
            used += need
            if used > k:
                return False
            running += need
            ends[min(i + 2 * r + 1, n)] -= need
    return True


def max_power(stations, r, k):
    n = len(stations)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stations[i]
    power = [prefix[min(i + r + 1, n)] - prefix[max(i - r, 0)] for i in range(n)]
    lo = min(power)
    hi = lo + k
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2
        if reachable(power, r, k, mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    fixed = [
        ([1, 2, 4, 5, 0], 1, 2),
        ([4, 4, 4, 4], 0, 3),
        ([0], 0, 0),
        ([0], 0, 1000000000),
        ([5, 0, 0, 0, 0, 0, 5], 1, 3),
        ([1, 0, 0, 0, 1], 4, 0),
        ([0, 0, 0, 0, 0, 0], 1, 4),
        ([100000, 0, 100000], 0, 1),
    ]
    for stations, r, k in fixed:
        print(f"{show(stations)} r {r} k {k} -> {max_power(stations, r, k)}")
    seed = [2528]
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random(seed) % 20 + 1
        stations = [next_random(seed) % 6 for _ in range(n)]
        r = next_random(seed) % n
        k = next_random(seed) % 21
        a = max_power(stations, r, k)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 random lists of up to 20 cities: total {total}, checksum {check}")
    stations = [next_random(seed) % 100001 for _ in range(100000)]
    for r in [0, 10, 10000]:
        print(f"10^5 cities, r {r}, k 10^9: {max_power(stations, r, 1000000000)}")


main()
