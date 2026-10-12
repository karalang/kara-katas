# Benchmark for #384: mirror of shuffle.kara (Fisher-Yates from the end).


class Solution:
    def __init__(self, nums):
        self.original = nums
        self.seed = 384

    def below(self, n):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return (self.seed // 65536) % n

    def shuffle(self):
        a = list(self.original)
        i = len(a) - 1
        while i > 0:
            j = self.below(i + 1)
            a[i], a[j] = a[j], a[i]
            i -= 1
        return a


def main():
    s = Solution([i * 7 % 1000 for i in range(1000)])
    checksum = 0
    for _ in range(250000):
        a = s.shuffle()
        total = 0
        for k in range(len(a)):
            total += a[k] * (k + 1)
        checksum = (checksum * 31 + total) % 1000000007
    print(f"250000 shuffles of 1000 values, checksum {checksum}")


main()
