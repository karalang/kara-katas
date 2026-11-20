# LeetCode #1748: Sum of Unique Elements -- the Python mirror of the ★ arm
# (unique.kara): one pass with a state per value.


def sum_of_unique(nums):
    seen = [0] * 101
    total = 0
    for x in nums:
        if seen[x] == 0:
            total += x
        elif seen[x] == 1:
            total -= x
        seen[x] = min(seen[x] + 1, 2)
    return total


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def batch(count, most, top, rng):
    total = 0
    check = 0
    for _ in range(count):
        n = rng.next() % most + 1
        nums = [rng.next() % top + 1 for _ in range(n)]
        answer = sum_of_unique(nums)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} arrays of up to {most} values from 1 to {top}: unique sums add to {total}, checksum {check}")


def main():
    print(sum_of_unique([1, 2, 3, 2]))
    print(sum_of_unique([1, 1, 1, 1, 1]))
    print(sum_of_unique([1, 2, 3, 4, 5]))
    print(sum_of_unique([100]))
    print(sum_of_unique(list(range(1, 101))))
    print(sum_of_unique(list(range(1, 101)) * 2))
    rng = Rng(1748)
    batch(3000, 10, 5, rng)
    batch(1000, 100, 50, rng)
    batch(1000, 100, 100, rng)


main()
