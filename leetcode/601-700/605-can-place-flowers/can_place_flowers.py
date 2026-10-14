# LeetCode #605: Can Place Flowers -- plant greedily.
#
# Mirrors can_place_flowers.kara: plant in every empty plot whose
# neighbours are empty, in a copy of the bed, and compare the count.


def can_place_flowers(flowerbed, n):
    bed = list(flowerbed)
    planted = 0
    for i in range(len(bed)):
        if bed[i] == 0 and (i == 0 or bed[i - 1] == 0) and (i == len(bed) - 1 or bed[i + 1] == 0):
            bed[i] = 1
            planted += 1
    return planted >= n


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(flowerbed, n):
    answer = "true" if can_place_flowers(flowerbed, n) else "false"
    print(f"{flowerbed}, n = {n} -> {answer}")


def largest(flowerbed):
    n = 0
    while can_place_flowers(flowerbed, n + 1):
        n += 1
    return n


def word(b):
    return "true" if b else "false"


def main():
    show([1, 0, 0, 0, 1], 1)
    show([1, 0, 0, 0, 1], 2)
    show([0], 1)
    show([1], 1)
    show([1], 0)
    show([0, 0], 2)
    show([0, 0, 0], 2)
    show([0, 0, 1, 0, 0], 2)
    show([1, 0, 0, 0, 0, 1], 2)
    show([1, 0, 1, 0, 1, 0, 1], 1)
    show([0, 1, 0, 1, 0, 1, 0], 0)
    empty = [0] * 20000
    print(f"20000 empty plots: n = 10000 -> {word(can_place_flowers(empty, 10000))}, n = 10001 -> {word(can_place_flowers(empty, 10001))}")
    seed = [605]
    total = 0
    checksum = 0
    for _ in range(300):
        size = 1 + step(seed) % 40
        bed = []
        for i in range(size):
            if step(seed) % 3 == 0 and (i == 0 or bed[i - 1] == 0):
                bed.append(1)
            else:
                bed.append(0)
        got = largest(bed)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random beds: largest n in all {total}, checksum {checksum}")


main()
