# Benchmark mirror of randomized_collection.kara (#381).


class RandomizedCollection:
    def __init__(self):
        self.vals = []
        self.slot = []
        self.positions = {}
        self.seed = 381

    def insert(self, val):
        p = len(self.vals)
        self.vals.append(val)
        lst = self.positions.setdefault(val, [])
        self.slot.append(len(lst))
        lst.append(p)
        return len(lst) == 1

    def remove(self, val):
        if val not in self.positions:
            return False
        p = self.positions[val].pop()
        if not self.positions[val]:
            del self.positions[val]
        last = len(self.vals) - 1
        if p < last:
            moved = self.vals[last]
            k = self.slot[last]
            self.vals[p] = moved
            self.slot[p] = k
            self.positions[moved][k] = p
        self.vals.pop()
        self.slot.pop()
        return True

    def get_random(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.vals[(self.seed // 65536) % len(self.vals)]

    def len(self):
        return len(self.vals)


def main():
    rc = RandomizedCollection()
    seed = 381
    checksum = 0
    for _ in range(20000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        op = (seed // 65536) % 3
        seed = (seed * 1103515245 + 12345) % 2147483648
        x = (seed // 64) % 100000
        if op == 0:
            v = 1 if rc.insert(x) else 0
        elif op == 1:
            v = 1 if rc.remove(x) else 0
        elif rc.vals:
            v = rc.get_random() + 2
        else:
            v = 7
        checksum = (checksum * 31 + v) % 1000000007
    print(f"checksum {checksum} size {rc.len()}")


main()
