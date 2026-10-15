# LeetCode #665: Non-decreasing Array -- fix each drop as it comes.
# Mirrors the ★ arm (non_decreasing_array.kara) and its test harness.


def check_possibility(nums):
    a = list(nums)
    fixes = 0
    for i in range(1, len(a)):
        if a[i] < a[i - 1]:
            fixes += 1
            if fixes > 1:
                return False
            if i < 2 or a[i - 2] <= a[i]:
                a[i - 1] = a[i]
            else:
                a[i] = a[i - 1]
    return True


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def word(b):
    return "true" if b else "false"


def show(nums):
    if len(nums) <= 12:
        print(f"[{','.join(str(x) for x in nums)}]: {word(check_possibility(nums))}")
    else:
        print(f"{len(nums)} numbers from {nums[0]}: {word(check_possibility(nums))}")


def rising(n, rng):
    v = []
    x = -100000
    for _ in range(n):
        v.append(x)
        x += rng.next() % 21
    return v


def main():
    for a in [[4, 2, 3], [4, 2, 1], [7], [1, 5, 2, 3], [1, 2, 4, 5, 3], [-1, 4, 2, 3],
              [3, 4, 2, 3], [5, 7, 1, 8], [2, 2, 2, 1, 2, 2], [1, 3, 2, 1]]:
        show(a)
    rng = Rng(665)
    v = rising(10000, rng)
    show(v)
    one = list(v)
    one[5000] = 100000
    show(one)
    one[9000] = -100000
    show(one)
    show([5000 - i for i in range(10000)])
    yes = 0
    s = 0
    for i in range(1000):
        n = 1 + rng.next() % 8
        a = [rng.next() % 4 for _ in range(n)]
        if check_possibility(a):
            yes += 1
            s = (s * 31 + i) % 1000000007
    print(f"1000 random arrays: {yes} can be sorted, checksum {s}")


main()
