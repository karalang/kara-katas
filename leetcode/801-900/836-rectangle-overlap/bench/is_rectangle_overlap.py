# Benchmark for #836: Rectangle Overlap -- the ★ arm (the two projections).
#
# Mirrors is_rectangle_overlap.kara: two axis-aligned rectangles overlap
# with positive area exactly when their shadows on the x axis overlap in
# more than a point and so do their shadows on the y axis.


def is_rectangle_overlap(rec1, rec2):
    left = max(rec1[0], rec2[0])
    right = min(rec1[2], rec2[2])
    bottom = max(rec1[1], rec2[1])
    top = min(rec1[3], rec2[3])
    return left < right and bottom < top


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


# a number below 2^32, from three draws
def big_random(seed):
    hi = next_random(seed) * 32768
    hi += next_random(seed)
    return hi * 4 + next_random(seed) % 4


def main():
    # 4096 rectangles drawn once in LeetCode's range, their corners
    # anywhere and their sides up to 2 * 10^9 >> (k % 8) for rectangle k,
    # so they run from the size of the range down to a 128th of it.
    # Round s tests each rectangle i against rectangle (i + s + 1) % 4096.
    n = 4096
    rounds = 100000
    seed = [836]
    rects = []
    for k in range(n):
        reach = 2000000000 >> (k % 8)
        x1 = big_random(seed) % 2000000000 - 1000000000
        y1 = big_random(seed) % 2000000000 - 1000000000
        x2 = min(x1 + 1 + big_random(seed) % reach, 1000000000)
        y2 = min(y1 + 1 + big_random(seed) % reach, 1000000000)
        rects.append([x1, y1, x2, y2])
    total = 0
    checksum = 0
    for s in range(rounds):
        overlapping = 0
        for i in range(n):
            if is_rectangle_overlap(rects[i], rects[(i + s + 1) % n]):
                overlapping += 1
        total += overlapping
        checksum = (checksum * 131 + overlapping) % 1000000007
    print(f"{rounds} rounds of {n} pairs: {total} overlapping, checksum {checksum}")


main()
