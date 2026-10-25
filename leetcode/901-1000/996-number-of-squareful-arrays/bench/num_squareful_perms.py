# Benchmark: LeetCode #996 Number of Squareful Arrays -- the ★ arm,
# backtracking over the sorted values, on random arrays of 12 values,
# LeetCode's largest. Mirrors num_squareful_perms.kara, .rs, .c and
# go-seq/.
import math


def is_square(s):
    r = math.isqrt(s)
    return r * r == s


def num_squareful_perms(nums):
    a = sorted(nums)
    n = len(a)
    used = [False] * n

    def place(depth, last):
        if depth == n:
            return 1
        count = 0
        for i in range(n):
            if used[i]:
                continue
            if i > 0 and a[i] == a[i - 1] and not used[i - 1]:
                continue
            if depth > 0 and not is_square(last + a[i]):
                continue
            used[i] = True
            count += place(depth + 1, a[i])
            used[i] = False
        return count

    return place(0, 0)


seed = 996


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# 12 values below 50, each making a square with the one before
def random_walk():
    nums = [next_random() % 50]
    for _ in range(11):
        v = nums[-1]
        options = []
        r = 0
        while r * r < v + 50:
            if r * r >= v:
                options.append(r * r - v)
            r += 1
        nums.append(options[next_random() % len(options)])
    return nums


def main():
    rounds = 300
    arrays = [random_walk() for _ in range(20)]
    found = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            got = num_squareful_perms(arrays[(r + i) % 20])
            found += got
            check = (check * 31 + got + 1) % 1000000007
    print(f"{rounds} rounds over 20 arrays of 12 values: {found} squareful permutations, checksum {check}")


main()
