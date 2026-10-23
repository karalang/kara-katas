# LeetCode #900: RLE Iterator -- bench program, Python.
#
# The offset arm (the encoding left as it is) over one encoding of
# 200,000 runs of 1 to 1,000 terms with values up to 10^9, built once. Each
# round moves the encoding into a fresh iterator, asks for 1 to 1,000
# terms at a time until the iterator answers -1, folds the answers into a
# checksum, takes the encoding back and changes one run's count.


class RLEIterator:
    def __init__(self, encoding):
        self.encoding = encoding
        self.i = 0
        self.used = 0

    def next(self, n):
        need = n
        while self.i < len(self.encoding):
            left = self.encoding[self.i] - self.used
            if left >= need:
                self.used += need
                return self.encoding[self.i + 1]
            need -= left
            self.i += 2
            self.used = 0
        return -1


seed = 900


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    runs = 200000
    rounds = 140
    encoding = []
    for _ in range(runs):
        encoding.append(1 + next_random() % 1000)
        encoding.append((next_random() * 32768 + next_random()) % 1000000001)
    check = 0
    calls = 0
    for rnd in range(rounds):
        it = RLEIterator(encoding)
        while True:
            got = it.next(1 + next_random() % 1000)
            calls += 1
            if got == -1:
                break
            check = (check * 31 + got) % 1000000007
        encoding = it.encoding
        encoding[2 * (rnd * 7919 % runs)] = 1 + next_random() % 1000
    print(f"{rounds} rounds over {runs} runs: {calls} calls, checksum {check}")


main()
