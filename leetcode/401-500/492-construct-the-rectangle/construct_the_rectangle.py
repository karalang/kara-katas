# LeetCode #492: Construct the Rectangle -- Python mirror of the ★ arm
# (down from the square root); see construct_the_rectangle.kara.
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


def show(name, area):
    print(f"{name}: {area} -> {construct_rectangle(area)}")


seed = 492


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("example 1", 4)
    show("example 2", 37)
    show("example 3", 122122)
    show("one", 1)
    show("a prime square", 49)
    show("twice a prime", 26)
    show("ten million", 10000000)
    show("the largest prime below ten million", 9999991)
    # 300 random areas from 1 to ten million.
    count = 300
    squares = 0
    thin = 0
    checksum = 0
    for _ in range(count):
        high = next_random()
        area = 1 + (high * 32768 + next_random()) % 10000000
        sides = construct_rectangle(area)
        if sides[0] == sides[1]:
            squares += 1
        if sides[1] == 1:
            thin += 1
        checksum = (checksum * 31 + sides[0] - sides[1]) % 1000000007
    print(f"{count} random areas: {squares} squares, {thin} of width 1, checksum {checksum}")


main()
