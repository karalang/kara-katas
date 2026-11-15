# LeetCode #2166: Design Bitset -- the Python mirror of bitset.kara: the
# bits beside a flag that says whether every bit is flipped and the count
# of ones.


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


# ---- test harness ---------------------------------------------------------

seed = 2166


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def replay(size, script):
    bits = Bitset(size)
    answers = ["null"]
    for kind, idx in script:
        if kind == 0:
            bits.fix(idx)
            answers.append("null")
        elif kind == 1:
            bits.unfix(idx)
            answers.append("null")
        elif kind == 2:
            bits.flip()
            answers.append("null")
        elif kind == 3:
            answers.append(str(bits.all()).lower())
        elif kind == 4:
            answers.append(str(bits.one()).lower())
        elif kind == 5:
            answers.append(str(bits.count()))
        else:
            answers.append(f'"{bits.to_string()}"')
    return answers


def show(size, script):
    print(f"Bitset({size}) -> [{', '.join(replay(size, script))}]")


def fold(check, answers):
    for answer in answers:
        for b in answer.encode():
            check = (check * 31 + b) % 1000000007
    return check


def main():
    show(5, [(0, 3), (0, 1), (2, 0), (3, 0), (1, 0), (2, 0), (4, 0), (1, 0), (5, 0), (6, 0)])
    show(1, [(0, 0), (3, 0), (2, 0), (4, 0), (5, 0), (6, 0), (2, 0), (6, 0)])
    show(4, [(2, 0), (3, 0), (1, 2), (5, 0), (0, 2), (0, 2), (3, 0), (6, 0)])
    show(6, [(1, 5), (0, 5), (2, 0), (2, 0), (0, 0), (5, 0), (4, 0), (6, 0)])
    calls = 0
    check = 0
    for _ in range(2000):
        size = next_random() % 8 + 1
        length = next_random() % 30 + 1
        script = []
        for _ in range(length):
            pick = next_random() % 13
            kind = [0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 4, 5, 6][pick]
            script.append((kind, next_random() % size))
        calls += length
        check = fold(check, replay(size, script))
    print(f"2000 scripts: {calls} calls, checksum {check}")
    size = 100000
    script = []
    for i in range(100000):
        if i % 20000 == 19999:
            script.append((6, 0))
        else:
            kind = next_random() % 6
            script.append((kind, (next_random() * 32768 + next_random()) % size))
    print(f"100000 calls on 100000 bits: checksum {fold(0, replay(size, script))}")


main()
