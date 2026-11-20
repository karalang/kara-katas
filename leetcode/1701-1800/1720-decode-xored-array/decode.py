# LeetCode #1720: Decode XORed Array -- mirrors decode.kara, the ★ arm:
# each value the one before it XORed with the code between them.


def decode(encoded, first):
    arr = [first]
    for e in encoded:
        arr.append(arr[-1] ^ e)
    return arr


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def batch(count, most, top):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        encoded = [wide() % (top + 1) for _ in range(n)]
        first = wide() % (top + 1)
        arr = decode(encoded, first)
        for v in arr:
            total += v
            check = (check * 31 + v) % 1000000007
        check = (check * 31 + n) % 1000000007
    print(f"{count} arrays of up to {most} codes up to {top}: values sum to {total}, checksum {check}")


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    # LeetCode's two examples, then one code, a code of 0, and the largest
    # values
    print(show(decode([1, 2, 3], 1)))
    print(show(decode([6, 2, 7, 3], 4)))
    print(show(decode([5], 0)))
    print(show(decode([0, 0], 7)))
    print(show(decode([100000, 1, 100000], 100000)))
    seed = 1720
    batch(3000, 12, 15)
    batch(300, 1000, 100000)
    batch(10, 10000, 100000)


main()
