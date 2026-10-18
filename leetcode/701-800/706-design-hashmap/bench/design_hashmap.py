# LeetCode #706 bench: the ★ arm in Python. See the .kara twin for the
# workload.

seed = 706


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


def main():
    found = 0
    checksum = 0
    for _ in range(5):
        for _ in range(10):
            m = MyHashMap()
            for _ in range(300000):
                op = next_random() % 3
                hi = next_random()
                lo = next_random()
                key = (hi * 32768 + lo) % 50000
                if op == 0:
                    vhi = next_random()
                    vlo = next_random()
                    m.put(key, (vhi * 32768 + vlo) % 1000000)
                elif op == 1:
                    value = m.get(key)
                    if value >= 0:
                        found += 1
                    checksum = (checksum * 31 + value + 1) % 1000000007
                else:
                    m.remove(key)
    print(f"5 rounds of 10 maps of 300000 calls: {found} found, checksum {checksum}")


main()
