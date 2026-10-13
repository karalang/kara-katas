# LeetCode #461: Hamming Distance -- Python mirror of hamming_distance.kara
# (the star arm, clearing the lowest set bit).


def hamming_distance(x, y):
    z = x ^ y
    count = 0
    while z != 0:
        z &= z - 1
        count += 1
    return count


def show(x, y):
    d = hamming_distance(x, y)
    print(f"hamming_distance({x}, {y}) = {d}")


seed = 461


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show(1, 4)
    show(3, 1)
    show(0, 0)
    show(0, 2147483647)
    show(2147483647, 2147483647)
    show(5, 10)
    show(1073741824, 0)
    show(1431655765, 715827882)
    show(123456789, 987654321)
    count = 300
    total = 0
    checksum = 0
    for i in range(count):
        a = next_random()
        b = next_random()
        c = next_random()
        x = ((a * 32768 + b) * 2 + c % 2) % 2147483648
        a = next_random()
        b = next_random()
        c = next_random()
        y = ((a * 32768 + b) * 2 + c % 2) % 2147483648
        if i % 3 == 1:
            a = next_random()
            b = next_random()
            c = next_random()
            y = y & ((a * 32768 + b) * 2) & (c * 65536)
        elif i % 3 == 2:
            a = next_random()
            b = next_random()
            y = x ^ (1 << (a % 31)) ^ (1 << (b % 31))
        d = hamming_distance(x, y)
        total += d
        checksum = (checksum * 31 + d * 7 + x % 1000) % 1000000007
    print(f"{count} random pairs: total distance {total}, checksum {checksum}")


main()
