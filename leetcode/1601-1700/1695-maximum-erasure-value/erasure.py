# LeetCode #1695: Maximum Erasure Value -- mirrors erasure.kara, the ★ arm:
# each value's last place and the prefix sums.


def maximum_unique_subarray(nums):
    last = [-1] * 10001
    prefix = [0] * (len(nums) + 1)
    start = 0
    best = 0
    for i, v in enumerate(nums):
        prefix[i + 1] = prefix[i] + v
        start = max(start, last[v] + 1)
        last[v] = i
        best = max(best, prefix[i + 1] - prefix[start])
    return best


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = seed.next() % most + 1
        nums = [seed.next() % top + 1 for _ in range(n)]
        answer = maximum_unique_subarray(nums)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} arrays of up to {most} values up to {top}: answers sum to {total}, checksum {check}")


def main():
    print(maximum_unique_subarray([4, 2, 4, 5, 6]))
    print(maximum_unique_subarray([5, 2, 1, 2, 5, 2, 1, 2, 5]))
    print(maximum_unique_subarray([1]))
    print(maximum_unique_subarray([3, 3, 3]))
    print(maximum_unique_subarray([1, 2, 3, 4, 5]))
    seed = Seed(1695)
    batch(3000, 12, 5, seed)
    batch(300, 1000, 100, seed)
    batch(10, 100000, 10000, seed)


main()
