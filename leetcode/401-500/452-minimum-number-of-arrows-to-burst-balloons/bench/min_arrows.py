# Benchmark for #452: mirror of min_arrows.kara (greedy by end) on 10
# random sets of 100,000 balloons over the 32-bit range, built once,
# then each counted 10 times.


def find_min_arrow_shots(points):
    by_end = sorted(points, key=lambda p: p[1])
    arrows = 0
    arrow = 0
    for start, end in by_end:
        if arrows == 0 or start > arrow:
            arrows += 1
            arrow = end
    return arrows


seed = 452


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    sets = 10
    n = 100000
    rounds = 10
    every = []
    for _ in range(sets):
        points = []
        for _ in range(n):
            r = next_random() * 65536
            r = (r + next_random()) * 2
            r += next_random() % 2
            start = r - 2147483648
            w = next_random() * 65536
            w = (w + next_random()) % 100000
            points.append((start, min(start + w, 2147483647)))
        every.append(points)
    total = 0
    checksum = 0
    for _ in range(rounds):
        for points in every:
            arrows = find_min_arrow_shots(points)
            total += arrows
            checksum = (checksum * 31 + arrows) % 1000000007
    print(f"{rounds} rounds on {sets} sets of {n}: {total} arrows, checksum {checksum}")


main()
