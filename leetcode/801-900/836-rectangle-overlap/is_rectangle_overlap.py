# Python mirror of the ★ arm plus harness for kata 836.

def is_rectangle_overlap(rec1, rec2):
    left = max(rec1[0], rec2[0])
    right = min(rec1[2], rec2[2])
    bottom = max(rec1[1], rec2[1])
    top = min(rec1[3], rec2[3])
    return left < right and bottom < top

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()

def random_rect(reach, side):
    x1 = wide_random() % (2 * reach) - reach
    y1 = wide_random() % (2 * reach) - reach
    w = 1 + wide_random() % side
    h = 1 + wide_random() % side
    return [x1, y1, x1 + w, y1 + h]

def fmt(v):
    return "[" + ", ".join(map(str, v)) + "]"

def show(rec1, rec2):
    print(f"rec1 = {fmt(rec1)}, rec2 = {fmt(rec2)} -> {str(is_rectangle_overlap(rec1, rec2)).lower()}")

def main():
    global seed
    show([0, 0, 2, 2], [1, 1, 3, 3])
    show([0, 0, 1, 1], [1, 0, 2, 1])
    show([0, 0, 1, 1], [2, 2, 3, 3])
    show([0, 0, 4, 4], [1, 1, 2, 2])
    show([1, 1, 2, 2], [0, 0, 4, 4])
    show([0, 1, 4, 2], [1, 0, 2, 4])
    show([0, 0, 1, 1], [1, 1, 2, 2])
    show([0, 0, 1, 1], [0, 1, 1, 2])
    show([0, 0, 5, 1], [2, -3, 3, 0])
    show([-3, -3, 3, 3], [-3, -3, 3, 3])
    show([-1000000000, -1000000000, 1000000000, 1000000000], [999999999, 999999999, 1000000000, 1000000000])
    show([-1000000000, -1000000000, 0, 1000000000], [0, -1000000000, 1000000000, 1000000000])
    seed = 836
    for label, reach, side in [("small", 4, 6), ("large", 500000000, 500000000)]:
        overlapping = 0
        check = 0
        for _ in range(3000):
            rec1 = random_rect(reach, side)
            rec2 = random_rect(reach, side)
            bit = 1 if is_rectangle_overlap(rec1, rec2) else 0
            overlapping += bit
            check = (check * 3 + bit) % 1000000007
        print(f"3000 {label} pairs: {overlapping} overlapping, checksum {check}")

main()
