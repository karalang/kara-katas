# LeetCode #565: Array Nesting -- Python mirror of the ★ arm (walk each
# cycle once); see array_nesting.kara.


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


# ---- test harness ---------------------------------------------------------

seed = 565


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(map(str, nums))}]: {array_nesting(nums)}")


def permutation(n):
    nums = list(range(n))
    i = n - 1
    while i > 0:
        j = step() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
        i -= 1
    return nums


def main():
    show([5, 4, 0, 3, 1, 6, 2])
    show([0, 1, 2])
    show([0])
    show([1, 0])
    show([4, 3, 2, 1, 0])
    show([1, 2, 3, 4, 5, 0])
    show([1, 0, 3, 4, 2, 6, 7, 8, 5])
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + step() % 50
        got = array_nesting(permutation(n))
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random permutations: total {total}, checksum {checksum}")
    n = 100000
    print(f"100000 in one cycle: {array_nesting([(i + 1) % n for i in range(n)])}")
    print(f"100000 fixed: {array_nesting(list(range(n)))}")
    print(f"100000 in pairs: {array_nesting([i ^ 1 for i in range(n)])}")
    print(f"100000 random: {array_nesting(permutation(n))}")


main()
