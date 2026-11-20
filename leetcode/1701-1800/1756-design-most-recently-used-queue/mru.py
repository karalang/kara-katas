# LeetCode #1756: Design Most Recently Used Queue -- mirrors mru.kara (the
# ★ arm): a list.


class MruQueue:
    def __init__(self, n):
        self.values = list(range(1, n + 1))

    def fetch(self, k):
        value = self.values.pop(k - 1)
        self.values.append(value)
        return value


seed = 1756


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, calls):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        queue = MruQueue(n)
        for _ in range(calls):
            k = next_random() % n + 1
            got = queue.fetch(k)
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"{count} queues of up to {most} values, {calls} fetches each: fetched values add to {total}, checksum {check}")


def show(values):
    print("[" + ", ".join(str(v) for v in values) + "]")


queue = MruQueue(8)
show([queue.fetch(3), queue.fetch(5), queue.fetch(2), queue.fetch(8)])
one = MruQueue(1)
show([one.fetch(1), one.fetch(1)])
last = MruQueue(4)
show([last.fetch(4), last.fetch(4), last.fetch(1), last.fetch(1)])
batch(3000, 6, 6)
batch(100, 2000, 2000)
