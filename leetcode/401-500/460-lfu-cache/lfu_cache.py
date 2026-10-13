# LeetCode #460: LFU Cache -- Python mirror of lfu_cache.kara (the star
# arm, a linked list per use count).
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


def run(capacity, ops):
    cache = LFUCache(capacity)
    answers = []
    for kind, key, value in ops:
        if kind == 0:
            cache.put(key, value)
        else:
            answers.append(cache.get(key))
    return answers


def show(name, capacity, ops):
    answers = run(capacity, ops)
    print(f"{name}: [{', '.join(str(a) for a in answers)}]")


seed = 460


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("example", 2, [(0, 1, 1), (0, 2, 2), (1, 1, 0), (0, 3, 3), (1, 2, 0), (1, 3, 0), (0, 4, 4), (1, 1, 0), (1, 3, 0), (1, 4, 0)])
    show("one slot", 1, [(0, 1, 10), (1, 1, 0), (0, 2, 20), (1, 1, 0), (1, 2, 0)])
    show("update keeps", 2, [(0, 1, 1), (0, 2, 2), (0, 1, 5), (0, 3, 3), (1, 1, 0), (1, 2, 0), (1, 3, 0)])
    show("tie to oldest", 3, [(0, 1, 1), (0, 2, 2), (0, 3, 3), (1, 3, 0), (1, 1, 0), (1, 2, 0), (0, 4, 4), (1, 3, 0), (1, 4, 0)])
    show("miss", 2, [(1, 7, 0), (0, 7, 70), (1, 7, 0), (1, 8, 0)])
    show("frequent stays", 2, [(0, 1, 1), (1, 1, 0), (1, 1, 0), (1, 1, 0), (0, 2, 2), (0, 3, 3), (0, 4, 4), (1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0)])
    show("put counts", 2, [(0, 1, 1), (0, 1, 2), (0, 2, 3), (0, 3, 4), (1, 1, 0), (1, 2, 0), (1, 3, 0)])
    count = 300
    hits = 0
    gets = 0
    checksum = 0
    for _ in range(count):
        a = next_random()
        b = next_random()
        capacity = 1 + a % [10, 100][b % 2]
        keys = 1 + next_random() % (2 * capacity + 1)
        length = 1 + next_random() % 300
        ops = []
        for _ in range(length):
            kind = next_random() % 2
            key = next_random() % keys
            value = next_random() % 100000
            ops.append((kind, key, value))
        for answer in run(capacity, ops):
            gets += 1
            if answer >= 0:
                hits += 1
            checksum = (checksum * 31 + answer + 2) % 1000000007
    print(f"{count} random sessions: {gets} gets, {hits} hits, checksum {checksum}")


main()
