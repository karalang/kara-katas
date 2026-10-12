# LeetCode #380: Insert Delete GetRandom O(1) -- mirror of
# randomized_set.kara.


class RandomizedSet:
    def __init__(self):
        self.vals = []
        self.index = {}
        self.seed = 380

    def insert(self, val):
        if val in self.index:
            return False
        self.index[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val):
        if val not in self.index:
            return False
        i = self.index.pop(val)
        last = self.vals.pop()
        if i < len(self.vals):
            self.vals[i] = last
            self.index[last] = i
        return True

    def get_random(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.vals[(self.seed // 65536) % len(self.vals)]


def b(x):
    return "true" if x else "false"


def main():
    s = RandomizedSet()
    print(f"example: insert 1 {b(s.insert(1))}, remove 2 {b(s.remove(2))}, insert 2 {b(s.insert(2))}")
    r = s.get_random()
    print(f"get_random is 1 or 2: {b(r == 1 or r == 2)}")
    print(f"remove 1 {b(s.remove(1))}, insert 2 {b(s.insert(2))}, get_random {s.get_random()}")
    t = RandomizedSet()
    print(f"remove from empty: {b(t.remove(5))}")
    print(f"negative values: insert -7 {b(t.insert(-7))}, insert -7 {b(t.insert(-7))}, get_random {t.get_random()}")
    print(f"remove the last value: remove -7 {b(t.remove(-7))}, insert -7 {b(t.insert(-7))}")
    u = RandomizedSet()
    for v in range(10):
        u.insert(v * v)
    u.remove(0)
    u.remove(81)
    u.remove(25)
    total = 0
    for _ in range(100):
        total += u.get_random()
    print(f"after removing from both ends and the middle: sum of 100 draws {total}")
    # Random workloads: 100 sets driven by 1,000 operations each over
    # values from -50 to 49, a third insert, a third remove, a third
    # get_random (only when the set is not empty).
    seed = 380
    checksum = 0
    for _ in range(100):
        rs = RandomizedSet()
        for _ in range(1000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            op = (seed // 65536) % 3
            seed = (seed * 1103515245 + 12345) % 2147483648
            x = (seed // 65536) % 100 - 50
            if op == 0:
                v = 1 if rs.insert(x) else 0
            elif op == 1:
                v = 1 if rs.remove(x) else 0
            elif rs.vals:
                v = rs.get_random() + 100
            else:
                v = 7
            checksum = (checksum * 31 + v) % 1000000007
    print(f"100 random workloads: checksum {checksum}")


main()
