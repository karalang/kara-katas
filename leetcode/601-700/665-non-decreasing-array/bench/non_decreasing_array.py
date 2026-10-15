# Benchmark for #665: fix each drop as it comes, as the Kara ★ arm.


def check_possibility(nums):
    a = list(nums)
    fixes = 0
    for i in range(1, len(a)):
        if a[i] < a[i - 1]:
            fixes += 1
            if fixes > 1:
                return False
            if i < 2 or a[i - 2] <= a[i]:
                a[i - 1] = a[i]
            else:
                a[i] = a[i - 1]
    return True


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    rng = Rng(665)
    arrays = []
    for t in range(16):
        v = []
        x = -100000
        for _ in range(10000):
            v.append(x)
            x += rng.next() % 21
        for _ in range(t % 3):
            at = rng.next() % 10000
            v[at] = rng.next() % 200001 - 100000
        arrays.append(v)
    rounds = 40000
    yes = 0
    s = 0
    for r in range(rounds):
        ok = check_possibility(arrays[r % 16])
        if ok:
            yes += 1
        s = (s * 31 + r * 2 + (1 if ok else 0)) % 1000000007
    print(f"16 arrays of 10000, {rounds} rounds: {yes} can be sorted, checksum {s}")


main()
