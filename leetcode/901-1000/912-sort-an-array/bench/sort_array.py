# LeetCode #912: Sort an Array -- bench program, Python.
#
# Heap sort on 500,000 numbers from -5 * 10^4 to 5 * 10^4, built once.
# Each round sorts a copy, folds a sample of the sorted values into a
# checksum and changes one number; 6 rounds.


def sift_down(a, start, end):
    root = start
    while True:
        child = 2 * root + 1
        if child >= end:
            return
        if child + 1 < end and a[child + 1] > a[child]:
            child += 1
        if a[root] >= a[child]:
            return
        a[root], a[child] = a[child], a[root]
        root = child


def sort_array(nums):
    a = list(nums)
    n = len(a)
    for parent in range(n // 2 - 1, -1, -1):
        sift_down(a, parent, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)
    return a


seed = 912


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 500000
    rounds = 6
    nums = [next_random() % 100001 - 50000 for _ in range(n)]
    check = 0
    for r in range(rounds):
        s = sort_array(nums)
        for i in range(r, n, 997):
            check = (check * 31 + s[i] + 50000) % 1000000007
        nums[r * 7919 % n] = next_random() % 100001 - 50000
    print(f"{rounds} rounds over {n} numbers: checksum {check}")


main()
