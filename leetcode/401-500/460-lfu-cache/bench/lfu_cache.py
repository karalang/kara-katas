# Benchmark for #460: mirror of lfu_cache.kara (the star arm, a linked
# list per use count) on the same workload.
#
# The nodes live in lists indexed by node number and link by index. The
# keys used c times form a circular list behind a sentinel node of their
# own, oldest first; `least` is the smallest count whose list is not
# empty. A node freed by an eviction is reused.

KEY, VALUE, COUNT, PREV, NEXT = range(5)


class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = []
        self.index = {}
        self.sentinels = {}
        self.least = 0
        self.free = -1

    def unlink(self, i):
        prev, nxt = self.nodes[i][PREV], self.nodes[i][NEXT]
        self.nodes[prev][NEXT] = nxt
        self.nodes[nxt][PREV] = prev

    def append(self, i, count):
        if count not in self.sentinels:
            s = len(self.nodes)
            self.nodes.append([-1, 0, count, s, s])
            self.sentinels[count] = s
        s = self.sentinels[count]
        last = self.nodes[s][PREV]
        self.nodes[i][COUNT] = count
        self.nodes[i][PREV] = last
        self.nodes[i][NEXT] = s
        self.nodes[last][NEXT] = i
        self.nodes[s][PREV] = i

    def is_empty(self, count):
        s = self.sentinels[count]
        return self.nodes[s][NEXT] == s

    def touch(self, i):
        count = self.nodes[i][COUNT]
        self.unlink(i)
        if self.least == count and self.is_empty(count):
            self.least = count + 1
        self.append(i, count + 1)

    def get(self, key):
        if key not in self.index:
            return -1
        i = self.index[key]
        self.touch(i)
        return self.nodes[i][VALUE]

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.index:
            i = self.index[key]
            self.nodes[i][VALUE] = value
            self.touch(i)
            return
        if len(self.index) == self.capacity:
            s = self.sentinels[self.least]
            victim = self.nodes[s][NEXT]
            self.unlink(victim)
            del self.index[self.nodes[victim][KEY]]
            self.free = victim
        if self.free >= 0:
            i = self.free
            self.free = -1
            self.nodes[i][KEY] = key
            self.nodes[i][VALUE] = value
        else:
            self.nodes.append([key, value, 0, -1, -1])
            i = len(self.nodes) - 1
        self.index[key] = i
        self.append(i, 1)
        self.least = 1


def main():
    capacity = 4096
    calls = 10000000
    seed = 460

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    cache = LFUCache(capacity)
    hits = 0
    checksum = 0
    for _ in range(calls):
        a = next_random() % 200
        b = next_random() % 200
        key = a * b
        if next_random() % 2 == 0:
            cache.put(key, next_random() % 1000000)
        else:
            answer = cache.get(key)
            if answer >= 0:
                hits += 1
            checksum = (checksum * 31 + answer + 2) % 1000000007
    print(f"{calls} calls on a cache of {capacity}: {hits} hits, checksum {checksum}")


main()
