# LeetCode #1656: Design an Ordered Stream -- the Python mirror of the ★
# arm: a slot per id and a pointer to the first id not yet returned.


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


# ---- the harness: the same as every arm's ---------------------------------

seed = 1656


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(chunk):
    return "[" + ", ".join(chunk) + "]"


def batch(count, most):
    check = 0
    chunks = 0
    values = 0
    for _ in range(count):
        n = next_random() % most + 1
        order = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        stream = OrderedStream(n)
        for id_key in order:
            value = "".join(chr(ord("a") + next_random() % 26) for _ in range(5))
            chunk = stream.insert(id_key, value)
            if chunk:
                chunks += 1
            for v in chunk:
                values += 1
                for b in v.encode():
                    check = (check * 31 + b) % 1000000007
    print(f"{count} streams of up to {most} pairs: {chunks} chunks, {values} values, checksum {check}")


stream = OrderedStream(5)
print(show(stream.insert(3, "ccccc")))
print(show(stream.insert(1, "aaaaa")))
print(show(stream.insert(2, "bbbbb")))
print(show(stream.insert(5, "eeeee")))
print(show(stream.insert(4, "ddddd")))
one = OrderedStream(1)
print(show(one.insert(1, "x")))
in_order = OrderedStream(3)
for id_key in range(1, 4):
    print(show(in_order.insert(id_key, f"v{id_key}")))
batch(3000, 10)
batch(100, 1000)
