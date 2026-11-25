# LeetCode #1288 bench, Python: the same sort and sweep, workload and
# checksum as remove_covered_intervals.kara.


def remove_covered_intervals(intervals):
    order = sorted(intervals, key=lambda iv: (iv[0], -iv[1]))
    kept = 0
    reach = 0
    for interval in order:
        if interval[1] > reach:
            kept += 1
            reach = interval[1]
    return kept


def main():
    seed = 1288
    pool = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        start = seed % 100000
        seed = (seed * 1103515245 + 12345) % 2147483648
        end = start + 1 + seed % (100000 - start)
        pool.append([start, end])
    check = 0
    for r in range(3000):
        at = (check + r * 7919) % 99001
        window = [iv[:] for iv in pool[at:at + 1000]]
        check = (check * 131 + remove_covered_intervals(window)) % 1000000007
    print(f"3000 windows of 1000 intervals: checksum {check}")


main()
