# LeetCode #2166: Design Bitset -- the benchmark's Python mirror of
# bitset.kara.


class Bitset:
    def __init__(self, size):
        self.bits = [False] * size
        self.flipped = False
        self.ones = 0

    def fix(self, idx):
        if self.bits[idx] == self.flipped:
            self.bits[idx] = not self.flipped
            self.ones += 1

    def unfix(self, idx):
        if self.bits[idx] != self.flipped:
            self.bits[idx] = self.flipped
            self.ones -= 1

    def flip(self):
        self.flipped = not self.flipped
        self.ones = len(self.bits) - self.ones

    def all(self):
        return self.ones == len(self.bits)

    def one(self):
        return self.ones > 0

    def count(self):
        return self.ones

    def to_string(self):
        return "".join("1" if bit != self.flipped else "0" for bit in self.bits)


seed = 2166


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    size = 100000
    bits = Bitset(size)
    check = 0
    for i in range(5000000):
        if i % 500000 == 499999:
            for b in bits.to_string().encode():
                check = (check * 31 + b) % 1000000007
            continue
        pick = next_random() % 16
        if pick < 7:
            bits.fix((next_random() * 32768 + next_random()) % size)
            answer = 0
        elif pick < 13:
            bits.unfix((next_random() * 32768 + next_random()) % size)
            answer = 0
        elif pick == 13:
            bits.flip()
            answer = 0
        elif pick == 14:
            answer = 2 if bits.all() else 1 if bits.one() else 0
        else:
            answer = bits.count()
        check = (check * 31 + answer) % 1000000007
    print(f"5000000 calls: checksum {check}")


main()
