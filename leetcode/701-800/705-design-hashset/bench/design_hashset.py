# LeetCode #705 bench: the ★ arm in Python. See the .kara twin for the
# workload.

seed = 705


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


def main():
    found = 0
    checksum = 0
    for _ in range(5):
        for _ in range(10):
            s = MyHashSet()
            for _ in range(300000):
                op = next_random() % 3
                hi = next_random()
                lo = next_random()
                key = (hi * 32768 + lo) % 50000
                if op == 0:
                    s.add(key)
                elif op == 1:
                    s.remove(key)
                else:
                    yes = s.contains(key)
                    if yes:
                        found += 1
                    checksum = (checksum * 3 + (1 if yes else 2)) % 1000000007
    print(f"5 rounds of 10 sets of 300000 calls: {found} found, checksum {checksum}")


main()
