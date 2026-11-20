# LeetCode #1725: Number Of Rectangles That Can Form The Largest Square
# -- the Python mirror of the ★ arm, rectangles.kara: one pass, the
# largest shorter side so far and how many rectangles give it.


def count_good_rectangles(rectangles):
    best = 0
    count = 0
    for r in rectangles:
        side = min(r[0], r[1])
        if side > best:
            best = side
            count = 1
        elif side == best:
            count += 1
    return count


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def wide(seed):
    return next_random(seed) * 32768 + next_random(seed)


def batch(count, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        rectangles = []
        for _ in range(n):
            l = wide(seed) % top + 1
            w = wide(seed) % top + 1
            rectangles.append([l, w])
        answer = count_good_rectangles(rectangles)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} problems of up to {most} rectangles with sides up to {top}: answers sum to {total}, checksum {check}")


def main():
    print(count_good_rectangles([[5, 8], [3, 9], [5, 12], [16, 5]]))
    print(count_good_rectangles([[2, 3], [3, 7], [4, 3], [3, 7]]))
    print(count_good_rectangles([[1000000000, 1]]))
    print(count_good_rectangles([[7, 7]] * 1000))
    seed = [1725]
    batch(3000, 8, 6, seed)
    batch(300, 1000, 20, seed)
    batch(300, 1000, 1000000000, seed)


main()
