# LeetCode #1340: Jump Game V -- Python mirror of the ★ arm: memoized
# depth-first search, each direction walked outward up to d steps and
# stopped at the first value not lower.
import sys

sys.setrecursionlimit(10000)


def max_jumps(arr, d):
    memo = [0] * len(arr)

    def most_from(i):
        if memo[i] > 0:
            return memo[i]
        best = 1
        for step in (-1, 1):
            j = i + step
            while 0 <= j < len(arr) and abs(j - i) <= d and arr[j] < arr[i]:
                best = max(best, 1 + most_from(j))
                j += step
        memo[i] = best
        return best

    return max(most_from(i) for i in range(len(arr)))


seed = 1340


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    e1 = max_jumps([6, 4, 14, 6, 8, 13, 9, 7, 10, 6, 12], 2)
    e2 = max_jumps([3, 3, 3, 3, 3], 3)
    e3 = max_jumps([7, 6, 5, 4, 3, 2, 1], 1)
    one = max_jumps([5], 1)
    rising = list(range(1, 1001))
    big = [1 + next_random() % 100000 for _ in range(1000)]
    print(f"{e1} {e2} {e3} {one} {max_jumps(rising, 1000)} {max_jumps(big, 1000)} {max_jumps(big, 10)}")
    check = 0
    for t in range(1000):
        n = 1 + next_random() % 200 if t % 10 == 0 else 1 + next_random() % 20
        top = 5 if t % 2 == 0 else 100000
        arr = [1 + next_random() % top for _ in range(n)]
        d = 1 + next_random() % n
        check = (check * 131 + max_jumps(arr, d)) % 1000000007
    print(f"1000 random arrays: checksum {check}")


main()
