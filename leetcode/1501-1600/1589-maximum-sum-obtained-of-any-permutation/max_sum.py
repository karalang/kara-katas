# LeetCode #1589: Maximum Sum Obtained of Any Permutation -- the Python
# mirror of max_sum.kara: a difference array of counts, both lists sorted
# and multiplied in pairs.


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


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top, asks, rng):
    check = 0
    for _ in range(count):
        n = rng.wide() % most + 1
        nums = [rng.wide() % (top + 1) for _ in range(n)]
        m = rng.wide() % asks + 1
        requests = []
        for _ in range(m):
            a = rng.wide() % n
            b = rng.wide() % n
            requests.append([min(a, b), max(a, b)])
        check = mix(check, max_sum_range_query(nums, requests))
    print(f"{count} problems of up to {most} values and {asks} requests: checksum {check}")


def main():
    examples = [
        ([1, 2, 3, 4, 5], [[1, 3], [0, 1]]),
        ([1, 2, 3, 4, 5, 6], [[0, 1]]),
        ([1, 2, 3, 4, 5, 10], [[0, 2], [1, 3], [1, 1]]),
        ([7], [[0, 0], [0, 0]]),
        ([0, 0, 9], [[0, 2]]),
        ([100000] * 100000, [[0, 99999], [0, 99999], [0, 99999]]),
    ]
    for nums, requests in examples:
        shown = f"[{nums[0]}; {len(nums)}]" if len(nums) > 10 else f"{nums}"
        print(f"{shown} {requests} -> {max_sum_range_query(nums, requests)}")
    rng = Rng(1589)
    batch(3000, 8, 9, 5, rng)
    batch(300, 1000, 100000, 1000, rng)
    batch(3, 100000, 100000, 100000, rng)


main()
