# LeetCode #537: Complex Number Multiplication -- split, then the
# schoolbook product. Mirrors complex_number_multiply.kara and its
# harness.


def parts(num):
    halves = num.split("+")
    return int(halves[0]), int(halves[1][:-1])


def complex_number_multiply(num1, num2):
    a, b = parts(num1)
    c, d = parts(num2)
    return f"{a * c - b * d}+{a * d + b * c}i"


# ---- test harness

class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_number(rng):
    re = rng.next() % 201 - 100
    im = rng.next() % 201 - 100
    return f"{re}+{im}i"


def show(a, b):
    print(f"({a}) * ({b}) = {complex_number_multiply(a, b)}")


def sum_of(s, start):
    h = start
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    show("1+1i", "1+1i")
    show("1+-1i", "1+-1i")
    show("0+1i", "0+1i")
    show("1+0i", "-7+3i")
    show("-1+0i", "-7+3i")
    show("0+0i", "100+100i")
    show("3+4i", "3+-4i")
    show("100+100i", "100+100i")
    show("-100+-100i", "100+-100i")
    show("-100+100i", "-100+100i")
    show("12+-34i", "-56+78i")
    rng = Rng(537)
    real = 0
    checksum = 0
    for i in range(3000):
        a = random_number(rng)
        if i % 10 == 0:
            plus = a.find("+")
            im = int(a[plus + 1:-1])
            b = f"{a[:plus]}+{-im}i"
        else:
            b = random_number(rng)
        p = complex_number_multiply(a, b)
        if p.endswith("+0i"):
            real += 1
        checksum = sum_of(p, checksum)
    print(f"3000 random pairs: {real} real, checksum {checksum}")
    checksum = 0
    for re in range(-100, 101):
        for im in range(-100, 101):
            checksum = sum_of(complex_number_multiply(f"{re}+{im}i", "-37+59i"), checksum)
    print(f"every number times -37+59i: checksum {checksum}")


main()
