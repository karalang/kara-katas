"""LeetCode #1619: Mean of Array After Removing Some Elements -- the bench in
Python, mirroring trim.kara: sort a copy, then the mean of the middle 90%."""
import math


def trim_mean(arr):
    s = sorted(arr)
    k = len(s) // 20
    kept = s[k:len(s) - k]
    return sum(kept) / len(kept)


def main():
    seed = 1619

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = [[(next_random() * 32768 + next_random()) % 100001 for _ in range(1000)] for _ in range(20000)]
    check = 0
    total = 0.0
    for arr in arrays:
        mean = trim_mean(arr)
        total += mean
        check = (check * 31 + math.floor(mean * 100000.0 + 0.5) + 1) % 1000000007
    print(f"20000 arrays of 1000 values: means sum to {total:.5f}, checksum {check}")


main()
