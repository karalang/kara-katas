# LeetCode #2141: Maximum Running Time of N Computers -- the Python mirror
# of running.kara's ★ arm.


def max_run_time(n, batteries):
    total = sum(batteries)
    low = 0
    high = total // n
    while low < high:
        mid = (low + high + 1) // 2
        usable = sum(min(b, mid) for b in batteries)
        if usable >= n * mid:
            low = mid
        else:
            high = mid - 1
    return low


seed = 2141


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(n, batteries):
    print(f"{n} [{', '.join(map(str, batteries))}] -> {max_run_time(n, batteries)}")


def main():
    show(2, [3, 3, 3])
    show(2, [1, 1, 1, 1])
    show(1, [5])
    show(3, [4, 9, 2])
    show(2, [100, 1, 1])
    show(1, [1000000000, 1000000000, 1000000000])
    total = 0
    check = 0
    for rnd in range(2000):
        count = next_random() % 12 + 1
        n = next_random() % count + 1
        top = [10, 1000000000][rnd % 2]
        batteries = []
        for _ in range(count):
            hi = next_random()
            batteries.append((hi * 32768 + next_random()) % top + 1)
        minutes = max_run_time(n, batteries)
        total += minutes
        check = (check * 31 + minutes % 1000000007 + n) % 1000000007
    print(f"2000 fleets: {total} minutes in all, checksum {check}")
    full = [1000000000] * 100000
    rand = []
    for _ in range(100000):
        hi = next_random()
        rand.append((hi * 32768 + next_random()) % 1000000000 + 1)
    x = max_run_time(100000, full)
    y = max_run_time(1, rand)
    z = max_run_time(50000, rand)
    print(f"100000 batteries: {x} all full, {y} for one computer, {z} for 50000")


main()
