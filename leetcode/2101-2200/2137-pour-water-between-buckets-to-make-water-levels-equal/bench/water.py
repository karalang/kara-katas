# LeetCode #2137: Pour Water Between Buckets to Make Water Levels Equal --
# the benchmark, the same algorithm as water.kara.

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


def main():
    lists = []
    for _ in range(10):
        lists.append([next_random() % 100001 for _ in range(100000)])
    total = 0
    check = 0
    for rnd in range(10):
        for l in range(10):
            hi = next_random()
            at = (hi * 32768 + next_random()) % 100000
            lists[l][at] = next_random() % 100001
            loss = next_random() % 100
            level = equalize_water(lists[l], loss)
            scaled = math.floor(level * 1048576.0 + 0.5)
            total += scaled
            check = (check * 31 + scaled + rnd) % 1000000007
    print(f"100 solves: {total} in all, in steps of 2^-20, checksum {check}")


main()
