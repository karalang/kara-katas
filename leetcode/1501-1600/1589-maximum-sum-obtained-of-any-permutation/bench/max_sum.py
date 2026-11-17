# LeetCode #1589: Maximum Sum Obtained of Any Permutation -- the bench in
# Python, mirroring max_sum.kara.


def max_sum_range_query(nums, requests):
    n = len(nums)
    asked = [0] * (n + 1)
    for a, b in requests:
        asked[a] += 1
        asked[b + 1] -= 1
    for i in range(1, n):
        asked[i] += asked[i - 1]
    del asked[n:]
    asked.sort()
    values = sorted(nums)
    total = 0
    for count, v in zip(asked, values):
        total = (total + count * v) % 1000000007
    return total


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def wide(self):
        a = self.next()
        return a * 32768 + self.next()


def main():
    rng = Rng(1589)
    n = 100000
    problems = []
    for _ in range(20):
        nums = [rng.wide() % 100001 for _ in range(n)]
        requests = []
        for _ in range(100000):
            a = rng.wide() % n
            b = rng.wide() % n
            requests.append([min(a, b), max(a, b)])
        problems.append((nums, requests))
    check = 0
    for nums, requests in problems:
        check = (check * 31 + max_sum_range_query(nums, requests) + 1) % 1000000007
    print(f"20 problems of 100000 values and 100000 requests: checksum {check}")


main()
