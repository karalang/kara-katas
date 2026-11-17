# LeetCode #1588: Sum of All Odd Length Subarrays -- the bench in Python,
# mirroring odd_subarrays.kara.


def sum_odd_length_subarrays(arr):
    n = len(arr)
    total = 0
    for i, v in enumerate(arr):
        through = (i + 1) * (n - i)
        total += (through + 1) // 2 * v
    return total


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    rng = Rng(1588)
    arrays = []
    for _ in range(200000):
        n = rng.next() % 100 + 1
        arrays.append([rng.next() % 1000 + 1 for _ in range(n)])
    check = 0
    total = 0
    for arr in arrays:
        answer = sum_odd_length_subarrays(arr)
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"200000 arrays of 1 to 100 values: total {total}, checksum {check}")


main()
