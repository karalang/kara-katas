# Benchmark for #492: Python mirror of the ★ arm (down from the square
# root); see construct_the_rectangle.kara.
import math


def construct_rectangle(area):
    width = int(math.sqrt(area))
    while width * width > area:
        width -= 1
    while (width + 1) * (width + 1) <= area:
        width += 1
    while area % width != 0:
        width -= 1
    return [area // width, width]


def main():
    # 200,000 random areas from 1 to ten million, built once, then each
    # solved once.
    seed = 492

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    areas = []
    for _ in range(200000):
        high = next_random()
        areas.append(1 + (high * 32768 + next_random()) % 10000000)
    squares = 0
    thin = 0
    checksum = 0
    for area in areas:
        sides = construct_rectangle(area)
        if sides[0] == sides[1]:
            squares += 1
        if sides[1] == 1:
            thin += 1
        checksum = (checksum * 31 + sides[0] - sides[1]) % 1000000007
    print(f"200000 areas: {squares} squares, {thin} of width 1, checksum {checksum}")


main()
