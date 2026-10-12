# LeetCode #381: Insert Delete GetRandom O(1) - Duplicates allowed --
# mirror of randomized_collection.kara.


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


def b(x):
    return "true" if x else "false"


def main():
    c = RandomizedCollection()
    print(f"example: insert 1 {b(c.insert(1))}, insert 1 {b(c.insert(1))}, insert 2 {b(c.insert(2))}")
    r = c.get_random()
    print(f"get_random is 1 or 2: {b(r == 1 or r == 2)}")
    print(f"remove 1 {b(c.remove(1))}, get_random {c.get_random()}")
    e = RandomizedCollection()
    print(f"remove from empty: {b(e.remove(5))}")
    a = [e.insert(-4) for _ in range(3)]
    print(f"three copies: insert {b(a[0])} {b(a[1])} {b(a[2])}, len {e.len()}")
    rs = [e.remove(-4) for _ in range(4)]
    print(f"remove them: {b(rs[0])} {b(rs[1])} {b(rs[2])} {b(rs[3])}, len {e.len()}, insert again {b(e.insert(-4))}")
    w = RandomizedCollection()
    w.insert(1)
    for _ in range(3):
        w.insert(2)
    twos = sum(1 for _ in range(400) if w.get_random() == 2)
    print(f"one 1 and three 2s: {twos} of 400 draws are 2")
    m = RandomizedCollection()
    for v in range(12):
        m.insert(v % 4)
    m.remove(0)
    m.remove(3)
    m.remove(1)
    m.remove(0)
    total = sum(m.get_random() for _ in range(100))
    print(f"after four removals: len {m.len()}, sum of 100 draws {total}")
    seed = 381
    checksum = 0
    most = 0
    for _ in range(100):
        rc = RandomizedCollection()
        for _ in range(1000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            op = (seed // 65536) % 10
            seed = (seed * 1103515245 + 12345) % 2147483648
            x = (seed // 65536) % 20 - 10
            if op < 4:
                v = 1 if rc.insert(x) else 0
            elif op < 7:
                v = 1 if rc.remove(x) else 0
            elif rc.vals:
                v = rc.get_random() + 100
            else:
                v = 7
            checksum = (checksum * 31 + v) % 1000000007
            most = max(most, rc.len())
    print(f"100 random workloads: checksum {checksum}, largest size {most}")


main()
