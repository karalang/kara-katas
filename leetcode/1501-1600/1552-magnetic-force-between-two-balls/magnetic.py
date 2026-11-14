# LeetCode #1552: Magnetic Force Between Two Balls -- the Python mirror of
# magnetic.kara, the ★ arm: a binary search on the answer, each gap checked
# by placing balls greedily. Prints byte-identical output.


def fits(srt, m, gap):
    placed = 1
    last = srt[0]
    for p in srt:
        if p - last >= gap:
            placed += 1
            last = p
    return placed >= m


def max_distance(position, m):
    srt = sorted(position)
    lo = 1
    hi = srt[-1] - srt[0]
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2
        if fits(srt, m, mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, widest):
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % (most - 1) + 2
        n = min(n, widest)
        m = next_random() % (n - 1) + 2
        taken = set()
        position = []
        while len(position) < n:
            p = (next_random() * 32768 + next_random()) % widest + 1
            if p not in taken:
                taken.add(p)
                position.append(p)
        check = mix(check, max_distance(position, m))
    print(f"{count} baskets of up to {most} positions up to {widest}: checksum {check}")


def main():
    global seed
    examples = [
        ([1, 2, 3, 4, 7], 3),
        ([5, 4, 3, 2, 1, 1000000000], 2),
        ([1, 2], 2),
        ([1, 2, 3, 4, 5], 5),
        ([1, 100, 101, 200], 3),
        ([10, 1, 7, 4], 4),
        ([1, 1000000000, 500000000, 2], 3),
    ]
    for position, m in examples:
        print(f"[{', '.join(map(str, position))}], m = {m} -> {max_distance(position, m)}")
    spread = [i * 10000 + 1 for i in range(100000)]
    print(f"100000 positions 10000 apart, m = 1000 -> {max_distance(spread, 1000)}")
    seed = 1552
    batch(3000, 12, 30)
    batch(300, 1000, 1000000000)
    batch(30, 100000, 1000000000)


main()
