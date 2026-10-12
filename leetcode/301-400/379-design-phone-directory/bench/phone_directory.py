# Benchmark for #379: mirror of phone_directory.kara.


class PhoneDirectory:
    def __init__(self, max_numbers):
        size = 1
        while size < max_numbers:
            size *= 2
        free = [0] * (2 * size)
        for n in range(max_numbers):
            free[size + n] = 1
        for i in range(size - 1, 0, -1):
            free[i] = free[2 * i] + free[2 * i + 1]
        self.size = size
        self.free = free

    def set(self, number, value):
        free = self.free
        i = self.size + number
        free[i] = value
        i //= 2
        while i >= 1:
            free[i] = free[2 * i] + free[2 * i + 1]
            i //= 2

    def get(self):
        free = self.free
        if free[1] == 0:
            return -1
        i = 1
        while i < self.size:
            i = 2 * i if free[2 * i] > 0 else 2 * i + 1
        number = i - self.size
        self.set(number, 0)
        return number

    def check(self, number):
        return self.free[self.size + number] == 1

    def release(self, number):
        self.set(number, 1)


def main():
    m = 10000
    d = PhoneDirectory(m)
    seed = 379
    checksum = 0
    for _ in range(20000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        op = (seed // 65536) % 4
        seed = (seed * 1103515245 + 12345) % 2147483648
        x = (seed // 65536) % m
        if op == 0:
            v = d.get() + 1
        elif op == 1:
            v = 1 if d.check(x) else 0
        else:
            d.release(x)
            v = 0
        checksum = (checksum * 31 + v) % 1000000007
    print(f"checksum {checksum}")


main()
