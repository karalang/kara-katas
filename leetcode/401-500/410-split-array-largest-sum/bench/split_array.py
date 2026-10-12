# Benchmark for #410: mirror of split_array.kara (binary search on the
# answer).
import sys


def pieces_needed(nums, cap):
    pieces = 1
    s = 0
    for x in nums:
        if s + x > cap:
            pieces += 1
            s = x
        else:
            s += x
    return pieces


def split_array(nums, k):
    lo = 0
    hi = 0
    for x in nums:
        if x > lo:
            lo = x
        hi += x
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if pieces_needed(nums, mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


seed = 410


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    n = 1000
    total = 0
    checksum = 0
    for _ in range(arrays):
        nums = []
        for _ in range(n):
            hi = step()
            lo = step()
            nums.append((hi * 32768 + lo) % 1000001)
        k = 1 + step() % 50
        answer = split_array(nums, k)
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"{arrays} arrays of {n} numbers: total {total}, checksum {checksum}")


main()
