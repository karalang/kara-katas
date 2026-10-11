# Benchmark for #368 -- mirror of largest_subset.kara.


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


def main():
    seed = 368
    total = 0
    checksum = 0
    for _ in range(200):
        taken = [False] * 100001
        nums = []
        while len(nums) < 1000:
            seed = (seed * 1103515245 + 12345) % 2147483648
            high = seed // 65536
            seed = (seed * 1103515245 + 12345) % 2147483648
            v = 1 + (high * 32768 + seed // 65536) % 100000
            if not taken[v]:
                taken[v] = True
                nums.append(v)
        out = largest_divisible_subset(nums)
        total += len(out)
        for v in out:
            checksum = (checksum * 31 + v) % 1000000007
    print(f"{total} numbers in the answers, checksum {checksum}")


main()
