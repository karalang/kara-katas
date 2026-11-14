# LeetCode #1552: Magnetic Force Between Two Balls -- bench: the ★ arm (a
# binary search on the answer, a greedy check) over 20 baskets of 100000
# distinct positions up to 10^9, built once, each asked 5 times with its own
# number of balls every time. Python mirror of magnetic.kara.


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


seed = 1552


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    baskets = []
    for _ in range(20):
        taken = set()
        position = []
        while len(position) < 100000:
            p = (next_random() * 32768 + next_random()) % 1000000000 + 1
            if p not in taken:
                taken.add(p)
                position.append(p)
        baskets.append(position)
    check = 0
    for p in range(5):
        for b in range(len(baskets)):
            m = (p * 20 + b) * 997 % 99999 + 2
            check = mix(check, max_distance(baskets[b], m))
    print(f"5 passes over 20 baskets of 100000 positions: checksum {check}")


main()
