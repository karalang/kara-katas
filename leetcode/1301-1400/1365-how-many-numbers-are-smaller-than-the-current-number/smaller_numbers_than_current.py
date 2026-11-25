# LeetCode #1365: How Many Numbers Are Smaller Than the Current Number --
# Python mirror of the ★ arm: the values counted and the counts summed,
# so below[v] holds how many values are less than v.


def smaller_numbers_than_current(nums):
    below = [0] * 102
    for x in nums:
        below[x + 1] += 1
    for v in range(1, 102):
        below[v] += below[v - 1]
    return [below[x] for x in nums]


seed = 1365


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    cases = [[8, 1, 2, 2, 3], [6, 5, 4, 8], [7, 7, 7, 7], [5], [100, 0, 100, 0]]
    print(" ".join(show(smaller_numbers_than_current(c)) for c in cases))
    check = 0
    total = 0
    for _ in range(2000):
        n = 2 + next_random() % 499
        nums = [next_random() % 101 for _ in range(n)]
        for c in smaller_numbers_than_current(nums):
            total += c
            check = (check * 131 + c) % 1000000007
    print(f"2000 random arrays: {total} smaller in all, checksum {check}")


main()
