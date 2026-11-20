# LeetCode #1685: Sum of Absolute Differences in a Sorted Array -- mirrors
# absolute.kara, the ★ arm: the sums on either side.


def sum_differences(nums):
    n = len(nums)
    total = sum(nums)
    before = 0
    result = []
    for i in range(n):
        x = nums[i]
        after = total - before - x
        result.append(x * i - before + after - x * (n - 1 - i))
        before += x
    return result


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
        n = seed.next() % (most - 1) + 2
        nums = sorted(seed.next() % top + 1 for _ in range(n))
        for v in sum_differences(nums):
            total += v
            check = (check * 31 + v) % 1000000007
    print(f"{count} arrays of up to {most} values up to {top}: answers sum to {total}, checksum {check}")


def main():
    print(sum_differences([2, 3, 5]))
    print(sum_differences([1, 4, 6, 8, 10]))
    print(sum_differences([7, 7, 7]))
    print(sum_differences([1, 10000]))
    print(sum_differences([1, 1, 2, 2, 2, 9]))
    seed = Seed(1685)
    batch(3000, 12, 10, seed)
    batch(300, 1000, 10000, seed)
    batch(10, 100000, 10000, seed)


main()
