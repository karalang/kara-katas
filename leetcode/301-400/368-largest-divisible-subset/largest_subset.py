# LeetCode #368: Largest Divisible Subset -- mirror of largest_subset.kara.


def largest_divisible_subset(nums):
    a = sorted(nums)
    n = len(a)
    size = [1] * n
    nxt = [-1] * n
    for i in reversed(range(n)):
        for k in range(i + 1, n):
            if a[k] % a[i] == 0 and size[k] + 1 > size[i]:
                size[i] = size[k] + 1
                nxt[i] = k
    start = 0
    for i in range(1, n):
        if size[i] > size[start]:
            start = i
    out = []
    at = start
    while at != -1:
        out.append(a[at])
        at = nxt[at]
    return out


def show(label, nums):
    print(f"{label}: {largest_divisible_subset(nums)}")


def main():
    show("example 1", [1, 2, 3])
    show("example 2", [1, 2, 4, 8])
    show("one number", [7])
    show("primes only", [7, 3, 5, 2])
    show("unsorted input", [8, 4, 1, 2, 16, 3])
    show("two chains of equal length", [2, 3, 4, 9])
    show("the longer chain starts higher", [4, 8, 16, 1, 3, 9, 27, 81])
    show("no 1, shared factors", [6, 12, 24, 36, 18, 9])
    show("large values", [1000000000, 2000000000, 500000000, 3, 7])
    show("1 to 1000", list(range(1, 1001)))
    seed = 368
    total = 0
    checksum = 0
    for _ in range(300):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + (seed // 65536) % 40
        taken = [False] * 501
        nums = []
        while len(nums) < n:
            seed = (seed * 1103515245 + 12345) % 2147483648
            v = 1 + (seed // 65536) % 500
            if not taken[v]:
                taken[v] = True
                nums.append(v)
        out = largest_divisible_subset(nums)
        total += len(out)
        for v in out:
            checksum = (checksum * 31 + v) % 1000000007
    print(f"300 random sets: {total} numbers in the answers, checksum {checksum}")


main()
