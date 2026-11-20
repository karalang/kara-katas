# LeetCode #1756: Design Most Recently Used Queue -- the bench (mru.kara
# in Python): a list.


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


count, n, calls = 10000, 2000, 2000
fetches = [next_random() % n + 1 for _ in range(calls)]
total = 0
check = 0
for r in range(count):
    queue = MruQueue(n)
    for k in fetches:
        got = queue.fetch(k)
        total += got
        check = (check * 31 + got + r) % 1000000007
print(f"{count} queues of {n} values, {calls} fetches each: fetched values add to {total}, checksum {check}")
