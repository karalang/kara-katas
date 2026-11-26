# LeetCode #1465 Maximum Area of a Piece of Cake After Horizontal and
# Vertical Cuts: a mirror of max_area.kara.


def widest(size, cuts):
    # the widest gap between two neighbouring cuts of `cuts`, the cake's
    # edges at 0 and `size` counted as cuts
    s = sorted(cuts)
    best = s[0]
    for i in range(1, len(s)):
        best = max(best, s[i] - s[i - 1])
    return max(best, size - s[-1])


def max_area(h, w, horizontal_cuts, vertical_cuts):
    # every piece is a gap one way by a gap the other, so the largest is
    # the widest gap each way multiplied
    return widest(h, horizontal_cuts) * widest(w, vertical_cuts) % 1000000007


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def cuts(k, size):
    out = [1 + (next_random() * 32768 + next_random()) % (size - 1) for _ in range(k)]
    out = sorted(set(out))
    for i in range(len(out) - 1, 0, -1):
        j = next_random() % (i + 1)
        out[i], out[j] = out[j], out[i]
    return out


def main():
    global seed
    f = max_area
    most = [c for c in range(1, 100001) if c != 50000]
    e = [f(5, 4, [1, 2, 4], [1, 3]), f(5, 4, [3, 1], [1]), f(5, 4, [3], [3]),
         f(1000000000, 1000000000, [1], [999999999]), f(2, 2, [1], [1]), f(100001, 100001, most, most)]
    print(" ".join(str(x) for x in e))
    seed = 1465
    across = cuts(100000, 1000000000)
    down = cuts(100000, 1000000000)
    print(f"100000 cuts: {f(1000000000, 1000000000, across, down)}")
    check = 0
    for _ in range(2000):
        h = 2 + (next_random() * 32768 + next_random()) % 999999999
        w = 2 + (next_random() * 32768 + next_random()) % 999999999
        a = cuts(1 + next_random() % 50, h)
        b = cuts(1 + next_random() % 50, w)
        check = (check * 31 + f(h, w, a, b)) % 1000000007
    print(f"2000 random cakes: checksum {check}")


main()
