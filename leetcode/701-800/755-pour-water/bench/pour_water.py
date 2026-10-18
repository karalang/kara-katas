# LeetCode 755 — Pour Water, bench: the ★ arm (one drop at a time),
# mirrored from pour_water.kara.


def pour_water(heights, volume, k):
    h = list(heights)
    n = len(h)
    for _ in range(volume):
        best = k
        for d in (-1, 1):
            i = k
            while 0 <= i + d < n and h[i + d] <= h[i]:
                if h[i + d] < h[best]:
                    best = i + d
                i += d
            if best != k:
                break
        h[best] += 1
    return h


seed = 755


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 6000
    water = 0
    check = 0
    for _ in range(rounds):
        heights = [next_random() % 100 for _ in range(100)]
        volume = 2000
        k = next_random() % 100
        for x in pour_water(heights, volume, k):
            water += x
            check = (check * 31 + x) % 1000000007
    print(f"{rounds} landscapes of 100 columns, 2000 drops each: {water} units in all, checksum {check}")


main()
