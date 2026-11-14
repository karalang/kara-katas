# LeetCode #2141: Maximum Running Time of N Computers -- the benchmark, the
# same algorithm as running.kara.

seed = 2141


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def max_run_time(n, batteries):
    total = sum(batteries)
    low, high = 0, total // n
    while low < high:
        mid = (low + high + 1) // 2
        usable = sum(b if b < mid else mid for b in batteries)
        if usable >= n * mid:
            low = mid
        else:
            high = mid - 1
    return low


def main():
    fleets = []
    for _ in range(10):
        batteries = []
        for _ in range(100000):
            hi = next_random()
            batteries.append((hi * 32768 + next_random()) % 1000000000 + 1)
        fleets.append(batteries)
    total = check = 0
    for rnd in range(20):
        for f in range(10):
            hi = next_random()
            at = (hi * 32768 + next_random()) % 100000
            hi = next_random()
            fleets[f][at] = (hi * 32768 + next_random()) % 1000000000 + 1
            minutes = max_run_time(10000 * (f + 1), fleets[f])
            total += minutes
            check = (check * 31 + minutes % 1000000007 + rnd) % 1000000007
    print(f"200 solves: {total} minutes in all, checksum {check}")


main()
