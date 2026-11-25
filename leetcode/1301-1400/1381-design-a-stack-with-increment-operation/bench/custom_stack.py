# LeetCode #1381 bench -- Python: the ★ arm: an increment is owed to the
# element k places up; a pop pays the top element what it is owed and
# hands the debt down to the one below.


class CustomStack:
    def __init__(self, max_size):
        self.max_size = max_size
        self.stack = []
        self.owed = []

    def push(self, x):
        if len(self.stack) < self.max_size:
            self.stack.append(x)
            self.owed.append(0)

    def pop(self):
        if not self.stack:
            return -1
        x = self.stack.pop()
        debt = self.owed.pop()
        if self.owed:
            self.owed[-1] += debt
        return x + debt

    def increment(self, k, val):
        reach = min(len(self.stack), k)
        if reach > 0:
            self.owed[reach - 1] += val


def main():
    seed = 1381
    check = 0
    for _ in range(2000):
        seed = (seed + check) % 2147483648
        s = CustomStack(1000)
        for _ in range(3000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            r = (seed // 65536) % 10
            if r < 4:
                seed = (seed * 1103515245 + 12345) % 2147483648
                s.push(1 + (seed // 65536) % 1000)
            elif r < 7:
                seed = (seed * 1103515245 + 12345) % 2147483648
                k = 1 + (seed // 65536) % 1000
                seed = (seed * 1103515245 + 12345) % 2147483648
                val = (seed // 65536) % 101
                s.increment(k, val)
            else:
                check = (check * 131 + s.pop() + 1) % 1000000007
    print(f"2000 rounds of 3000 calls on a stack of 1000: checksum {check}")


main()
