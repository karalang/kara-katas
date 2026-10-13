# Benchmark for #537: the star arm (split, then the schoolbook product);
# see ../README.md section Benchmarks. Mirrors complex_number_multiply.kara.


def parts(num):
    halves = num.split("+")
    return int(halves[0]), int(halves[1][:-1])


def complex_number_multiply(num1, num2):
    a, b = parts(num1)
    c, d = parts(num2)
    return f"{a * c - b * d}+{a * d + b * c}i"


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    rng = Rng(537)
    nums = []
    for _ in range(2000):
        re = rng.next() % 201 - 100
        im = rng.next() % 201 - 100
        nums.append(f"{re}+{im}i")
    n = len(nums)
    rounds = 2500
    real = 0
    length = 0
    for r in range(rounds):
        for i in range(n):
            p = complex_number_multiply(nums[i], nums[(i * 7 + r) % n])
            if p.endswith("+0i"):
                real += 1
            length += len(p)
    print(f"{n} numbers, {rounds} rounds: {real} real, length {length}")


main()
