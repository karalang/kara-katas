# LeetCode #1560: Most Visited Sector in a Circular Track -- bench: the ★
# arm (the sectors from the first on to the last, wrapping past n) over
# 20000 tracks of up to 100 sectors and 100 legs, built once, each asked
# 100 times.
# Python mirror of sectors.kara.


def most_visited(n, rounds):
    start = rounds[0]
    end = rounds[-1]
    if start <= end:
        return list(range(start, end + 1))
    return list(range(1, end + 1)) + list(range(start, n + 1))


seed = 1560


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    tracks = []
    for _ in range(20000):
        n = next_random() % 99 + 2
        m = next_random() % 100 + 1
        rounds = [next_random() % n + 1]
        for _ in range(m):
            at = rounds[-1]
            rounds.append((at - 1 + next_random() % (n - 1) + 1) % n + 1)
        tracks.append((n, rounds))
    check = 0
    total = 0
    for p in range(100):
        for t, (n, rounds) in enumerate(tracks):
            sectors = most_visited(n, rounds)
            total += len(sectors)
            check = mix(check, sectors[(p * 7 + t) % len(sectors)])
    print(f"100 passes over 20000 tracks: {total} sectors, checksum {check}")


main()
