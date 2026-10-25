# LeetCode #996: Number of Squareful Arrays -- mirror of the ★ arm
# (num_squareful_perms.kara), backtracking over the sorted values.
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
            # of equal values, take the first one not yet used
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


def random_values(n, pool, walk):
    nums = [next_random() % pool]
    for _ in range(1, n):
        v = nums[-1]
        options = []
        r = 0
        while r * r < v + pool:
            if r * r >= v:
                options.append(r * r - v)
            r += 1
        if walk and options:
            nums.append(options[next_random() % len(options)])
        else:
            nums.append(next_random() % pool)
    return nums


def main():
    cases = [
        [1, 17, 8],
        [2, 2, 2],
        [0],
        [1, 3],
        [2, 2, 3],
        [0, 0, 0, 1, 1],
        [1, 8, 17, 19, 6],
        [10, 6, 3, 15, 1],
        [0, 1, 0, 1, 0],
        [1000000000, 1000000000],
    ]
    for nums in cases:
        text = "[" + ",".join(str(v) for v in nums) + "]"
        print(f"nums = {text} -> {num_squareful_perms(nums)}")
    print(f"twelve 2s: {num_squareful_perms([2] * 12)}")
    print(f"twelve 0s: {num_squareful_perms([0] * 12)}")
    triangular = [t * (t + 1) // 2 for t in range(1, 13)]
    print(f"the first twelve triangular numbers: {num_squareful_perms(triangular)}")
    print(f"six 0s and six 1s: {num_squareful_perms([0] * 6 + [1] * 6)}")
    print(f"twelve values that never pair: {num_squareful_perms([3 * i + 2 for i in range(12)])}")
    # random arrays: half random values below pool, half a random walk
    # where each value makes a square with the one before, when one can
    for count, most, pool in ((300, 4, 20), (3000, 8, 50), (300, 12, 30)):
        values = 0
        found = 0
        check = 0
        for _ in range(count):
            n = 1 + next_random() % most
            nums = random_values(n, pool, next_random() % 2 == 0)
            values += n
            got = num_squareful_perms(nums)
            found += got
            check = (check * 31 + got + 1) % 1000000007
        print(f"{count} random arrays of {values} values: {found} squareful permutations, checksum {check}")

main()
