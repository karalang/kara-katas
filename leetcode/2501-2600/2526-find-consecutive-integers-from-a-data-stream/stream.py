# LeetCode #2526: Find Consecutive Integers from a Data Stream -- Python
# mirror of the ★ arm (stream.kara): a counter of the run of matches; the
# same harness and output.


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


def answers(value, k, nums):
    stream = DataStream(value, k)
    return "".join("T" if stream.consec(num) else "F" for num in nums)


def show(value, k, nums):
    print(f"{value} {k} [{', '.join(map(str, nums))}] -> {answers(value, k, nums)}")


def main():
    show(4, 3, [4, 4, 4, 3])
    show(1, 1, [1, 2, 1, 1])
    show(5, 2, [5, 6, 5, 5, 5, 6, 5])
    show(9, 4, [9, 9, 9])
    show(1000000000, 2, [1000000000, 1000000000, 1])
    show(2, 3, [1, 2, 2, 2, 2, 1, 2, 2, 2])
    trues = 0
    check = 0
    for _ in range(2000):
        value = next_random() % 3 + 1
        k = next_random() % 6 + 1
        n = next_random() % 60 + 1
        nums = [next_random() % 3 + 1 for _ in range(n)]
        for c in answers(value, k, nums):
            t = 1 if c == "T" else 0
            trues += t
            check = (check * 31 + t + 1) % 1000000007
    print(f"2000 random streams: {trues} true, checksum {check}")
    spaced = [8 if i % 50 == 49 else 7 for i in range(100000)]
    print(f"10^5, k 10^5, one in 50 not value: {answers(7, 100000, spaced).count('T')} true")
    print(f"10^5, k 100, all value: {answers(7, 100, [7] * 100000).count('T')} true")
    halves = [next_random() % 2 + 7 for _ in range(100000)]
    print(f"10^5, k 3, half value: {answers(7, 3, halves).count('T')} true")


main()
