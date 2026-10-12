# Benchmark for #380: mirror of randomized_set.kara (the open-addressing
# arm). Slots hold None or (value, position).
MUL = 0x9E3779B97F4A7C15  # -7046029254386353131 as an unsigned 64-bit word
MASK64 = (1 << 64) - 1


class RandomizedSet:
    def __init__(self):
        self.vals = []
        self.slots = [None] * 8
        self.seed = 380

    def home(self, val):
        return (((val * MUL) & MASK64) >> 32) & (len(self.slots) - 1)

    def find(self, val):
        slots = self.slots
        mask = len(slots) - 1
        i = self.home(val)
        while True:
            s = slots[i]
            if s is None or s[0] == val:
                return i
            i = (i + 1) & mask

    def set_position(self, val, pos):
        self.slots[self.find(val)] = (val, pos)

    def grow(self):
        old = self.slots
        self.slots = [None] * (2 * len(old))
        for s in old:
            if s is not None:
                self.set_position(s[0], s[1])

    def insert(self, val):
        if self.slots[self.find(val)] is not None:
            return False
        if 2 * (len(self.vals) + 1) > len(self.slots):
            self.grow()
        self.set_position(val, len(self.vals))
        self.vals.append(val)
        return True

    def delete_slot(self, i):
        slots = self.slots
        mask = len(slots) - 1
        gap = i
        j = (i + 1) & mask
        slots[gap] = None
        while True:
            s = slots[j]
            if s is None:
                return
            h = self.home(s[0])
            stays = (gap < h <= j) if gap <= j else (gap < h or h <= j)
            if not stays:
                slots[gap] = s
                slots[j] = None
                gap = j
            j = (j + 1) & mask

    def remove(self, val):
        i = self.find(val)
        s = self.slots[i]
        if s is None:
            return False
        pos = s[1]
        self.delete_slot(i)
        last = self.vals.pop()
        if pos < len(self.vals):
            self.vals[pos] = last
            self.set_position(last, pos)
        return True

    def get_random(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.vals[(self.seed // 65536) % len(self.vals)]


def main():
    s = RandomizedSet()
    seed = 380
    checksum = 0
    for _ in range(20000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        op = (seed // 65536) % 3
        seed = (seed * 1103515245 + 12345) % 2147483648
        x = (seed // 64) % 200000
        if op == 0:
            v = 1 if s.insert(x) else 0
        elif op == 1:
            v = 1 if s.remove(x) else 0
        elif s.vals:
            v = s.get_random()
        else:
            v = 7
        checksum = (checksum * 31 + v) % 1000000007
    print(f"checksum {checksum} size {len(s.vals)}")


main()
