# LeetCode #670: Maximum Swap -- the last place of each digit.
# Mirrors the ★ arm (maximum_swap.kara) and its test harness.


def digits_of(num):
    d = []
    x = num
    while x > 0:
        d.append(x % 10)
        x //= 10
    if not d:
        d.append(0)
    d.reverse()
    return d


def number_of(d):
    x = 0
    for v in d:
        x = x * 10 + v
    return x


def maximum_swap(num):
    d = digits_of(num)
    last = [-1] * 10
    for i in range(len(d)):
        last[d[i]] = i
    for i in range(len(d)):
        v = 9
        while v > d[i]:
            if last[v] > i:
                j = last[v]
                d[j] = d[i]
                d[i] = v
                return number_of(d)
            v -= 1
    return num


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    for n in [2736, 9973, 0, 7, 10, 98368, 1993, 109090, 99901, 115, 4321,
              1234, 120, 12345678, 87654321, 98765432, 100000000, 99999999]:
        print(f"{n}: {maximum_swap(n)}")
    raised = 0
    s = 0
    for n in range(100000):
        m = maximum_swap(n)
        if m != n:
            raised += 1
        s = (s * 31 + m) % 1000000007
    print(f"0 to 99999: {raised} raised, checksum {s}")
    rng = Rng(670)
    s = 0
    for _ in range(10000):
        a = rng.next()
        b = rng.next()
        s = (s * 31 + maximum_swap((a * 32768 + b) % 100000001)) % 1000000007
    print(f"10000 random: checksum {s}")


main()
