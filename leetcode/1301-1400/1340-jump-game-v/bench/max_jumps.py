# LeetCode #1340 bench in Python: the ★ arm (memoized depth-first search,
# each direction walked outward up to d steps and stopped at the first
# value not lower) on the same 20 arrays of 1000 values and 20 passes.
import sys

sys.setrecursionlimit(10000)


def max_jumps(arr, d):
    n = len(arr)
    memo = [0] * n

    def most_from(i):
        if memo[i] > 0:
            return memo[i]
        best = 1
        for step in (-1, 1):
            j = i + step
            while 0 <= j < n and abs(j - i) <= d and arr[j] < arr[i]:
                best = max(best, 1 + most_from(j))
                j += step
        memo[i] = best
        return best

    best = 0
    for i in range(n):
        best = max(best, most_from(i))
    return best


seed = 1340


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 1000
    arrays = []
    for a in range(20):
        if a % 2 == 0:
            arrays.append([1 + next_random() % 100000 for _ in range(n)])
        else:
            arrays.append([100 * k + 1 + next_random() % 100 for k in range(n)])
    check = 0
    for pass_ in range(20):
        for a in range(20):
            arr = arrays[a]
            arr[check % n] = 1 + (check // 7) % 100000
            d = 1000 if a % 2 == 0 else 300
            answer = max_jumps(arr, d)
            check = (check * 31 + answer + pass_) % 1000000007
    print(f"20 passes over 20 arrays of 1000: checksum {check}")


main()
