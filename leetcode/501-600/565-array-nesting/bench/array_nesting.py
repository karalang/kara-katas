# Benchmark for #565: Python mirror of the ★ arm (walk each cycle once);
# see array_nesting.kara.


def array_nesting(nums):
    n = len(nums)
    visited = [False] * n
    best = 0
    for start in range(n):
        if visited[start]:
            continue
        length = 0
        i = start
        while not visited[i]:
            visited[i] = True
            i = nums[i]
            length += 1
        best = max(best, length)
    return best


# ---- benchmark ---------------------------------------------------------------

seed = 565


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 20
    rounds = 100
    n = 100000
    perms = []
    for g in range(count):
        nums = list(range(n))
        if g % 2 == 0:
            for i in range(n - 1, 0, -1):
                hi = step()
                j = (hi * 32768 + step()) % (i + 1)
                nums[i], nums[j] = nums[j], nums[i]
        else:
            start = 0
            while start < n:
                length = min(1 + step() % 2000, n - start)
                for j in range(length):
                    nums[start + j] = start + (j + 1) % length
                start += length
        perms.append(nums)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            got = array_nesting(perms[(rnd * 7 + g) % count])
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} permutations of {n}, {rounds} rounds: total {total}, checksum {checksum}")


main()
