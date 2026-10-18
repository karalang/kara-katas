# LeetCode #705: Design HashSet -- buckets of chained keys.
#
# A mirror of design_hashset.kara (the ★ arm) and its harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class MyHashSet:
    def __init__(self):
        self.buckets = [[] for _ in range(1009)]

    def add(self, key):
        b = self.buckets[key % 1009]
        if key not in b:
            b.append(key)

    def remove(self, key):
        b = self.buckets[key % 1009]
        for i in range(len(b)):
            if b[i] == key:
                b[i] = b[-1]
                b.pop()
                return

    def contains(self, key):
        return key in self.buckets[key % 1009]


def run(ops, keys):
    s = MyHashSet()
    out = []
    for op, key in zip(ops, keys):
        if op == 0:
            s.add(key)
            out.append("null")
        elif op == 1:
            s.remove(key)
            out.append("null")
        else:
            out.append("true" if s.contains(key) else "false")
    return out


def show(ops, keys):
    names = ["add", "remove", "contains"]
    calls = [f"{names[op]}({key})" for op, key in zip(ops, keys)]
    print(f"{', '.join(calls)}: [{', '.join(run(ops, keys))}]")


def random_calls(n, top):
    ops, keys = [], []
    for _ in range(n):
        ops.append(next_random() % 3)
        a = next_random()
        b = next_random()
        keys.append((a * 32768 + b) % top)
    return ops, keys


def checksum(answers):
    total = 0
    yes = 0
    for a in answers:
        v = 1 if a == "true" else 2 if a == "false" else 3
        if a == "true":
            yes += 1
        total = (total * 7 + v) % 1000000007
    return total * 100000 + yes


def main():
    global seed
    show([0, 0, 2, 2, 0, 2, 1, 2], [1, 2, 1, 3, 2, 2, 2, 2])
    show([2, 0, 0, 2, 2, 1, 2, 2], [0, 0, 1000000, 0, 1000000, 0, 0, 1000000])
    show([1, 2, 0, 1, 1, 2, 0, 2], [5, 5, 5, 5, 5, 5, 5, 5])
    show([0, 0, 0, 1, 2, 2, 2, 0, 2], [0, 1009, 2018, 1009, 0, 1009, 2018, 3027, 3027])
    show([0, 0, 1, 2, 2, 2], [64, 128, 64, 64, 128, 192])
    seed = 705
    for top in [1000001, 100]:
        ops, keys = random_calls(10000, top)
        print(f"10000 calls on keys below {top}: checksum {checksum(run(ops, keys))}")
    ops = [0] * 5000 + [1] * 2500 + [2] * 2500
    keys = list(range(5000)) + [2 * k + 1 for k in range(2500)]
    for k in range(2500):
        keys.append(2 * k + next_random() % 2)
    print(f"5000 added, odd ones removed, 2500 looked up: checksum {checksum(run(ops, keys))}")
    total = 0
    for _ in range(300):
        n = 1 + next_random() % 200
        top = 1 + next_random() % 3000
        ops, keys = random_calls(n, top)
        total = (total * 31 + checksum(run(ops, keys))) % 1000000007
    print(f"300 random sequences: checksum {total}")


main()
