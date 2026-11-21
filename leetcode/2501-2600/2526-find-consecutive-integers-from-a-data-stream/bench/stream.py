# LeetCode #2526: Find Consecutive Integers from a Data Stream -- benchmark
# mirror of the ★ arm (stream.kara): the same numbers and passes, each a
# fresh stream fed every number.


class DataStream:
    def __init__(self, value, k):
        self.value = value
        self.k = k
        self.run = 0

    def consec(self, num):
        self.run = self.run + 1 if num == self.value else 0
        return self.run >= self.k


seed = 2526


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    nums = [next_random() % 3 + 1 for _ in range(100000)]
    passes = 1250
    check = 0
    for p in range(passes):
        stream = DataStream(check % 3 + 1, check % 8 + 1)
        trues = 0
        for num in nums:
            if stream.consec(num):
                trues += 1
        check = (check * 31 + trues + p) % 1000000007
    print(f"{passes} passes over 10^5 numbers: checksum {check}")


main()
