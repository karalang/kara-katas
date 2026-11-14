# LeetCode #2137: Pour Water Between Buckets to Make Water Levels Equal --
# the Python mirror of water.kara's ★ arm.

import math


def equalize_water(buckets, loss):
    keep = (100 - loss) / 100.0
    low = 0.0
    high = float(max(buckets))
    for _ in range(64):
        mid = (low + high) / 2.0
        spare = 0.0
        need = 0.0
        for b in buckets:
            w = float(b)
            if w > mid:
                spare += (w - mid) * keep
            else:
                need += mid - w
        if spare >= need:
            low = mid
        else:
            high = mid
    return low


seed = 2137


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(buckets, loss):
    print(f"[{', '.join(map(str, buckets))}] {loss} -> {equalize_water(buckets, loss):.5f}")


def main():
    show([1, 2, 7], 80)
    show([2, 4, 6], 50)
    show([3, 3, 3, 3], 40)
    show([5], 99)
    show([0, 0, 0], 10)
    show([1, 2, 3, 4], 0)
    show([0, 100000], 99)
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 10 + 1
        top = [10, 100, 100000][rnd % 3]
        buckets = [next_random() % (top + 1) for _ in range(n)]
        loss = next_random() % 100
        level = equalize_water(buckets, loss)
        scaled = math.floor(level * 1048576.0 + 0.5)
        total += scaled
        check = (check * 31 + scaled + n) % 1000000007
    print(f"2000 lists: {total} in all, in steps of 2^-20, checksum {check}")
    big = [next_random() % 100001 for _ in range(100000)]
    x = equalize_water(big, 0)
    y = equalize_water(big, 50)
    z = equalize_water(big, 99)
    print(f"100000 buckets: {x:.5f} at no loss, {y:.5f} at half, {z:.5f} at 99")


main()
