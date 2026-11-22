# LeetCode #2528: Maximize the Minimum Powered City -- benchmark mirror of
# the ★ arm (power.kara): 10^5 cities built once, then the passes, each
# asking for the answer with an `r` and a `k` the checksum picks.


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


seed = 2528


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    stations = [next_random() % 100001 for _ in range(100000)]
    passes = 20
    check = 0
    for p in range(passes):
        r = check % 100
        k = 1000000000 - check % 1000
        check = (check * 31 + max_power(stations, r, k) + p) % 1000000007
    print(f"{passes} passes over 100000 cities: checksum {check}")


main()
