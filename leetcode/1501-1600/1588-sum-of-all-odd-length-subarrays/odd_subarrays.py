# LeetCode #1588: Sum of All Odd Length Subarrays -- the Python mirror of
# odd_subarrays.kara: each value times its count of odd subarrays.


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


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, least, most, top, rng):
    check = 0
    total = 0
    for _ in range(count):
        n = least + rng.next() % (most - least + 1)
        arr = [rng.next() % top + 1 for _ in range(n)]
        answer = sum_odd_length_subarrays(arr)
        total += answer
        check = mix(check, answer)
    print(f"{count} arrays of {least} to {most} values up to {top}: total {total}, checksum {check}")


def main():
    examples = [[1, 4, 2, 5, 3], [1, 2], [10, 11, 12], [7], [1, 1, 1, 1], [1000] * 100]
    for arr in examples:
        shown = f"[{arr[0]}; {len(arr)}]" if len(arr) > 10 else f"{arr}"
        print(f"{shown} -> {sum_odd_length_subarrays(arr)}")
    rng = Rng(1588)
    batch(3000, 1, 10, 10, rng)
    batch(300, 1, 100, 1000, rng)
    batch(30, 100, 100, 1000, rng)


main()
