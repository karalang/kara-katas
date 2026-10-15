# Benchmark for #677: the keys kept sorted, as the Kara sorted arm.


class MapSum:
    def __init__(self):
        self.keys = []
        self.vals = []

    def insert(self, key, val):
        at = lower_bound(self.keys, key)
        if at < len(self.keys) and self.keys[at] == key:
            self.vals[at] = val
        else:
            self.keys.insert(at, key)
            self.vals.insert(at, val)

    def sum(self, prefix):
        total = 0
        i = lower_bound(self.keys, prefix)
        while i < len(self.keys) and self.keys[i].startswith(prefix):
            total += self.vals[i]
            i += 1
        return total


def lower_bound(keys, word):
    lo = 0
    hi = len(keys)
    while lo < hi:
        mid = (lo + hi) // 2
        if keys[mid] < word:
            lo = mid + 1
        else:
            hi = mid
    return lo


seed = 677


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(most):
    n = 1 + next_random() % most
    return "".join(chr(97 + next_random() % 3) for _ in range(n))


def main():
    rounds = 100
    calls = 2000
    s = 0
    for _ in range(rounds):
        m = MapSum()
        for _ in range(calls):
            key = random_word(12)
            m.insert(key, 1 + next_random() % 1000)
        for _ in range(calls):
            s = (s * 31 + m.sum(random_word(3))) % 1000000007
    print(f"{rounds} rounds of {calls} inserts and {calls} sums: checksum {s}")


main()
