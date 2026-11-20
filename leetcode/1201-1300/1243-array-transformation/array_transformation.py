# LeetCode #1243: Array Transformation -- mirrors array_transformation.kara.


def transform_array(arr):
    cur = list(arr)
    while True:
        nxt = list(cur)
        for i in range(1, len(cur) - 1):
            if cur[i] < cur[i - 1] and cur[i] < cur[i + 1]:
                nxt[i] += 1
            elif cur[i] > cur[i - 1] and cur[i] > cur[i + 1]:
                nxt[i] -= 1
        if nxt == cur:
            return cur
        cur = nxt


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    print(fmt(transform_array([6, 2, 3, 4])))
    print(fmt(transform_array([1, 6, 3, 4, 3, 5])))
    rng = Rng(1243)
    check = 0
    total = 0
    for _ in range(1000):
        n = rng.next() % 98 + 3
        arr = [rng.next() % 100 + 1 for _ in range(n)]
        for v in transform_array(arr):
            total += v
            check = (check * 131 + v) % 1000000007
    print(f"1000 random arrays: total {total}, checksum {check}")
    zigzag = [1 if i % 2 == 0 else 100 for i in range(100)]
    saw = [i * 37 % 100 + 1 for i in range(100)]
    z = transform_array(zigzag)
    s = transform_array(saw)
    print(f"zigzag: {z[0]} {z[1]} {z[50]} {z[98]} {z[99]}, by 37: {s[0]} {s[1]} {s[50]} {s[98]} {s[99]}")


main()
