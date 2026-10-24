# LeetCode #984: String Without AAA or BBB -- mirror of the ★ arm
# (str_without_3a3b.kara), greedy, reading the tail.


def str_without_3a3b(a, b):
    s = ""
    left_a, left_b = a, b
    while left_a > 0 or left_b > 0:
        if s.endswith("aa"):
            write_a = False
        elif s.endswith("bb"):
            write_a = True
        else:
            write_a = left_a >= left_b
        if write_a:
            s += "a"
            left_a -= 1
        else:
            s += "b"
            left_b -= 1
    return s


seed = 984


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shown(s):
    if len(s) > 24:
        return f"{s[:12]}...{s[-6:]} ({len(s)} letters)"
    return s


def show(a, b):
    print(f"a = {a}, b = {b} -> {shown(str_without_3a3b(a, b))}")


def possible(a, b):
    return a + b > 0 and a <= 2 * b + 2 and b <= 2 * a + 2


class Tally:
    def __init__(self):
        self.letters = 0
        self.doubled = 0
        self.check = 0

    def add(self, s):
        prev = ""
        for c in s:
            if c == prev:
                self.doubled += 1
            prev = c
            self.check = (self.check * 31 + (1 if c == "a" else 2)) % 1000000007
        self.letters += len(s)
        self.check = (self.check * 31 + 3) % 1000000007

    def line(self, what):
        return f"{what}: {self.letters} letters, {self.doubled} doubled, checksum {self.check}"


def main():
    show(1, 2)
    show(4, 1)
    show(1, 0)
    show(0, 2)
    show(3, 3)
    show(6, 2)
    show(2, 6)
    show(5, 3)
    show(3, 5)
    show(100, 100)
    for count, top in [(300, 10), (3000, 100)]:
        t = Tally()
        for _ in range(count):
            while True:
                a = next_random() % (top + 1)
                b = next_random() % (top + 1)
                if possible(a, b):
                    break
            t.add(str_without_3a3b(a, b))
        print(t.line(f"{count} random pairs up to {top}"))
    t = Tally()
    count = 0
    for a in range(101):
        for b in range(101):
            if possible(a, b):
                t.add(str_without_3a3b(a, b))
                count += 1
    print(t.line(f"all {count} pairs up to 100"))


main()
