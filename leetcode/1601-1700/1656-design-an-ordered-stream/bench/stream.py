# LeetCode #1656: Design an Ordered Stream -- the bench's Python mirror:
# the ★ arm on 2000 random streams of 1000 pairs, each inserted in a
# random order with a value of five random letters, all drawn first.


class OrderedStream:
    def __init__(self, n):
        self.slots = [None] * (n + 1)
        self.next = 1

    def insert(self, id_key, value):
        self.slots[id_key] = value
        chunk = []
        while self.next < len(self.slots) and self.slots[self.next] is not None:
            chunk.append(self.slots[self.next])
            self.next += 1
        return chunk


seed = 1656


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


n = 1000
streams = []
for _ in range(2000):
    order = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    pairs = []
    for id_key in order:
        pairs.append((id_key, "".join(chr(ord("a") + next_random() % 26) for _ in range(5))))
    streams.append(pairs)
check = 0
chunks = 0
for pairs in streams:
    stream = OrderedStream(n)
    for id_key, value in pairs:
        chunk = stream.insert(id_key, value)
        if chunk:
            chunks += 1
        for v in chunk:
            for b in v.encode():
                check = (check * 31 + b) % 1000000007
print(f"2000 streams of 1000 pairs: {chunks} chunks, checksum {check}")
