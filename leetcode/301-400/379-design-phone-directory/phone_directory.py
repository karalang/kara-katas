# LeetCode #379: Design Phone Directory -- mirror of phone_directory.kara.
# get() hands out the smallest free number.
import bisect


class PhoneDirectory:
    def __init__(self, max_numbers):
        self.free = list(range(max_numbers))  # kept sorted

    def get(self):
        if not self.free:
            return -1
        return self.free.pop(0)

    def check(self, number):
        i = bisect.bisect_left(self.free, number)
        return i < len(self.free) and self.free[i] == number

    def release(self, number):
        if not self.check(number):
            bisect.insort(self.free, number)


def b(x):
    return "true" if x else "false"


def main():
    d = PhoneDirectory(3)
    print(f"example: get {d.get()}, get {d.get()}, check 2 {b(d.check(2))}, get {d.get()}, check 2 {b(d.check(2))}")
    d.release(2)
    print(f"after release 2: check 2 {b(d.check(2))}, get {d.get()}")
    one = PhoneDirectory(1)
    print(f"one number: get {one.get()}, get {one.get()}, check 0 {b(one.check(0))}")
    one.release(0)
    one.release(0)
    print(f"released twice: get {one.get()}, get {one.get()}")
    e = PhoneDirectory(5)
    e.release(3)
    print(f"releasing a free number: get {e.get()}, get {e.get()}, get {e.get()}, get {e.get()}, get {e.get()}, get {e.get()}")
    f = PhoneDirectory(6)
    for _ in range(6):
        f.get()
    f.release(4)
    f.release(1)
    print(f"smallest free first: get {f.get()}, get {f.get()}, get {f.get()}")
    # Random directories of up to 1,000 numbers, each driven by 1,000
    # operations: half gets, a quarter checks, a quarter releases.
    seed = 379
    checksum = 0
    for _ in range(100):
        seed = (seed * 1103515245 + 12345) % 2147483648
        m = 1 + (seed // 65536) % 1000
        d = PhoneDirectory(m)
        for _ in range(1000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            op = (seed // 65536) % 4
            seed = (seed * 1103515245 + 12345) % 2147483648
            x = (seed // 65536) % m
            if op <= 1:
                v = d.get() + 1
            elif op == 2:
                v = 1 if d.check(x) else 0
            else:
                d.release(x)
                v = 0
            checksum = (checksum * 31 + v) % 1000000007
    print(f"100 random directories: checksum {checksum}")


main()
