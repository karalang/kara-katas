# LeetCode #706: Design HashMap -- buckets of chained pairs.
#
# A mirror of design_hashmap.kara (the ★ arm) and its harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class MyHashMap:
    def __init__(self):
        self.buckets = [[] for _ in range(1009)]

    def put(self, key, value):
        b = self.buckets[key % 1009]
        for i in range(len(b)):
            if b[i][0] == key:
                b[i] = (key, value)
                return
        b.append((key, value))

    def get(self, key):
        for k, v in self.buckets[key % 1009]:
            if k == key:
                return v
        return -1

    def remove(self, key):
        b = self.buckets[key % 1009]
        for i in range(len(b)):
            if b[i][0] == key:
                b[i] = b[-1]
                b.pop()
                return


def run(ops, keys, values):
    m = MyHashMap()
    out = []
    for op, key, value in zip(ops, keys, values):
        if op == 0:
            m.put(key, value)
            out.append(None)
        elif op == 1:
            out.append(m.get(key))
        else:
            m.remove(key)
            out.append(None)
    return out


def show(ops, keys, values):
    calls = []
    for op, key, value in zip(ops, keys, values):
        if op == 0:
            calls.append(f"put({key}, {value})")
        elif op == 1:
            calls.append(f"get({key})")
        else:
            calls.append(f"remove({key})")
    shown = ["null" if a is None else str(a) for a in run(ops, keys, values)]
    print(f"{', '.join(calls)}: [{', '.join(shown)}]")


def big():
    a = next_random()
    b = next_random()
    return a * 32768 + b


def random_calls(n, top):
    ops, keys, values = [], [], []
    for _ in range(n):
        ops.append(next_random() % 3)
        keys.append(big() % top)
        values.append(big() % 1000001)
    return ops, keys, values


def checksum(answers):
    total = 0
    for a in answers:
        v = 1000002 if a is None else a + 1
        total = (total * 31 + v) % 1000000007
    return total


def main():
    global seed
    show([0, 0, 1, 1, 0, 1, 2, 1], [1, 2, 1, 3, 2, 2, 2, 2], [1, 2, 0, 0, 1, 0, 0, 0])
    show([1, 0, 0, 1, 1, 0, 1], [0, 0, 1000000, 0, 1000000, 0, 0], [0, 0, 1000000, 0, 0, 7, 0])
    show([2, 1, 0, 2, 2, 1, 0, 1], [5, 5, 5, 5, 5, 5, 5, 5], [0, 0, 9, 0, 0, 0, 3, 0])
    show([0, 0, 0, 2, 1, 1, 1, 0, 1], [0, 1009, 2018, 1009, 0, 1009, 2018, 1009, 1009], [10, 20, 30, 0, 0, 0, 0, 40, 0])
    seed = 706
    for top in [1000001, 100]:
        ops, keys, values = random_calls(10000, top)
        print(f"10000 calls on keys below {top}: checksum {checksum(run(ops, keys, values))}")
    ops = [0] * 5000 + [2] * 2500 + [1] * 2500
    keys = list(range(5000)) + [2 * k + 1 for k in range(2500)]
    values = [k * 200 for k in range(5000)] + [0] * 5000
    for k in range(2500):
        keys.append(2 * k + next_random() % 2)
    print(f"5000 put, odd ones removed, 2500 read: checksum {checksum(run(ops, keys, values))}")
    total = 0
    for _ in range(300):
        n = 1 + next_random() % 200
        top = 1 + next_random() % 3000
        ops, keys, values = random_calls(n, top)
        total = (total * 31 + checksum(run(ops, keys, values))) % 1000000007
    print(f"300 random sequences: checksum {total}")


main()
