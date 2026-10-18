# LeetCode 755 — Pour Water, mirror of the ★ arm (one drop at a time) and
# its harness.


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


def show(heights, volume, k):
    after = pour_water(heights, volume, k)
    print(f"{heights}, V = {volume}, K = {k} -> {after}")


def main():
    show([2, 1, 1, 2, 1, 2, 2], 4, 3)
    show([1, 2, 3, 4], 2, 2)
    show([3, 1, 3], 5, 1)
    show([5], 3, 0)
    show([1, 1, 1, 1], 0, 2)
    show([0, 0, 0, 0, 0], 7, 2)
    show([4, 3, 2, 1, 0], 6, 0)
    show([0, 1, 2, 3, 4], 6, 4)
    show([2, 0, 2, 0, 2], 3, 2)
    show([3, 2, 1, 2, 1, 2, 3], 9, 3)
    water = 0
    check = 0
    for _ in range(200):
        n = 1 + next_random() % 100
        heights = [next_random() % 100 for _ in range(n)]
        volume = next_random() % 2001
        k = next_random() % n
        for x in pour_water(heights, volume, k):
            water += x
            check = (check * 31 + x) % 1000000007
    print(f"200 random landscapes: {water} units of ground and water in all, checksum {check}")


main()
