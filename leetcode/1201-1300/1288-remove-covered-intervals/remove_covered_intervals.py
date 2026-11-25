# LeetCode #1288: Remove Covered Intervals -- Python mirror of the ★ arm
# and its harness.


def remove_covered_intervals(intervals):
    order = sorted(intervals, key=lambda iv: (iv[0], -iv[1]))
    kept = 0
    reach = 0
    for start, end in order:
        if end > reach:
            kept += 1
            reach = end
    return kept


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, top):
    out = []
    while len(out) < n:
        a = (next_random() * 32768 + next_random()) % (top + 1)
        b = (next_random() * 32768 + next_random()) % (top + 1)
        if a == b:
            continue
        interval = [min(a, b), max(a, b)]
        if interval not in out:
            out.append(interval)
    return out


def main():
    global seed
    shown = [
        remove_covered_intervals([[1, 4], [3, 6], [2, 8]]),
        remove_covered_intervals([[1, 4], [2, 3]]),
        remove_covered_intervals([[0, 10], [5, 12]]),
        remove_covered_intervals([[3, 10], [4, 10], [5, 11]]),
        remove_covered_intervals([[1, 2], [1, 4], [3, 4]]),
    ]
    print(" ".join(str(k) for k in shown))
    seed = 1288
    big = drawn(1000, 100000)
    nested = [[i, 2000 - i] for i in range(1000)]
    chain = [[i, i + 1000] for i in range(1000)]
    kept = [remove_covered_intervals(big), remove_covered_intervals(nested), remove_covered_intervals(chain)]
    print(f"10^3 intervals: {kept[0]} {kept[1]} {kept[2]}")
    check = 0
    total = 0
    for i in range(2000):
        n = 1 + next_random() % 30
        top = 10 if i % 3 == 0 else 100 if i % 3 == 1 else 100000
        k = remove_covered_intervals(drawn(n, top))
        total += k
        check = (check * 131 + k) % 1000000007
    print(f"2000 random cases: {total} in all, checksum {check}")


main()
