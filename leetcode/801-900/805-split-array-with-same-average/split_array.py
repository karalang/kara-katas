# LeetCode 805 -- Split Array With Same Average: mirrors the harness of
# split_array.kara with the ★ arm's sums by size.
seed = 805


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def split_array_same_average(nums):
    n = len(nums)
    total = sum(nums)
    half = n // 2
    sums = [set() for _ in range(half + 1)]
    sums[0].add(0)
    for x in nums:
        for k in range(half, 0, -1):
            for s in list(sums[k - 1]):
                sums[k].add(s + x)
    for k in range(1, half + 1):
        if total * k % n == 0 and total * k // n in sums[k]:
            return True
    return False


def show(nums):
    out = "[" + ", ".join(str(v) for v in nums) + "]"
    print(f"{out} -> {str(split_array_same_average(nums)).lower()}")


def main():
    show([1, 2, 3, 4, 5, 6, 7, 8])
    show([3, 1])
    show([5])
    show([0, 0])
    show([4, 4, 4, 4])
    show([0, 13, 13, 7, 5, 0, 10, 19, 5])
    show([10000] + [0] * 28 + [9999])
    show([2, 0, 5, 6, 16, 12, 15, 12, 4])
    yes = 0
    check = 0
    for i in range(300):
        n = 1 + next_random() % 16
        cap = 4 * (1 + next_random() % 100)
        nums = [next_random() % cap for _ in range(n)]
        can = split_array_same_average(nums)
        if can:
            yes += 1
        check = (check * 131 + (1 if can else 2) + i) % 1000000007
    print(f"300 random arrays: {yes} can be split, checksum {check}")


main()
