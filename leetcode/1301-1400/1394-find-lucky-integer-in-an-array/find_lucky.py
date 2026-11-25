# LeetCode #1394: Find Lucky Integer in an Array -- Python mirror of the
# ★ arm: a count for each value from 1 to 500, read from the top down.


def find_lucky(arr):
    count = [0] * 501
    for x in arr:
        count[x] += 1
    for x in range(500, 0, -1):
        if count[x] == x:
            return x
    return -1


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n values, each either drawn from 1 to `most` or, a third of the time,
# a value placed so its count may match it: a lucky value is planted by
# writing x exactly x times first, when there is room
def drawn(n, most):
    out = []
    x = 1 + next_random() % most
    if x <= n and next_random() % 2 == 0:
        out = [x] * x
    while len(out) < n:
        out.append(1 + next_random() % most)
    # shuffled, so the planted run is spread out
    for i in range(len(out) - 1, 0, -1):
        j = next_random() % (i + 1)
        out[i], out[j] = out[j], out[i]
    return out


def main():
    global seed
    shown = [
        find_lucky([2, 2, 3, 4]),
        find_lucky([1, 2, 2, 3, 3, 3]),
        find_lucky([2, 2, 2, 3, 3]),
        find_lucky([1]),
        find_lucky([5, 5, 5, 5, 5]),
        find_lucky([7]),
    ]
    print(" ".join(str(x) for x in shown))
    seed = 1394
    big = [find_lucky([500] * 500), find_lucky([499] * 499 + [1]), find_lucky(drawn(500, 500)), find_lucky(drawn(500, 30))]
    print("500 values: " + " ".join(str(x) for x in big))
    check = 0
    total = 0
    for c in range(2000):
        n = 1 + next_random() % 60
        most = 1 + next_random() % (12 if c % 2 == 0 else 500)
        got = find_lucky(drawn(n, most))
        total += got
        check = (check * 131 + got + 1) % 1000000007
    print(f"2000 random arrays: {total} in all, checksum {check}")


main()
