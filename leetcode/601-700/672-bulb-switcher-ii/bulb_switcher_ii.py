# LeetCode #672: Bulb Switcher II -- the cases worked out.
# Mirrors the ★ arm (bulb_switcher_ii.kara) and its test harness.


def flip_lights(n, m):
    if m == 0:
        return 1
    if n == 1:
        return 2
    if n == 2:
        return 3 if m == 1 else 4
    if m == 1:
        return 4
    if m == 2:
        return 7
    return 8


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    for n, m in [(1, 1), (2, 1), (3, 1)]:
        print(f"n={n} m={m}: {flip_lights(n, m)}")
    for n in range(1, 9):
        print(f"n={n}: " + " ".join(str(flip_lights(n, m)) for m in range(7)))
    for n, m in [(1000, 1000), (1000, 0), (1, 1000), (2, 999)]:
        print(f"n={n} m={m}: {flip_lights(n, m)}")
    rng = Rng(672)
    s = 0
    for _ in range(1000):
        n = 1 + rng.next() % 1000
        m = rng.next() % 1001
        s = (s * 31 + flip_lights(n, m)) % 1000000007
    print(f"1000 random cases: checksum {s}")


main()
