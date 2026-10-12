# LeetCode #384: Shuffle an Array -- Fisher-Yates. Mirrors shuffle.kara.
import math


class Solution:
    def __init__(self, nums):
        self.original = nums
        self.seed = 384

    # A number from 0 to n - 1.
    def below(self, n):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return (self.seed // 65536) % n

    def reset(self):
        return list(self.original)

    def shuffle(self):
        a = list(self.original)
        i = len(a) - 1
        while i > 0:
            j = self.below(i + 1)
            a[i], a[j] = a[j], a[i]
            i -= 1
        return a


def b(x):
    return "true" if x else "false"


def same_values(a, original):
    return sorted(a) == sorted(original)


def rank(a):
    r = 0
    for i in range(len(a)):
        smaller = sum(1 for j in range(i + 1, len(a)) if a[j] < a[i])
        r = r * (len(a) - i) + smaller
    return r


def fair(n, draws):
    orders = math.factorial(n)
    nums = list(range(n))
    s = Solution(list(nums))
    got = [0] * orders
    for _ in range(draws):
        a = s.shuffle()
        if not same_values(a, nums):
            return False
        got[rank(a)] += 1
    e = draws / orders
    chi = 0.0
    for k in range(orders):
        d = got[k] - e
        chi += d * d / e
    dof = float(orders - 1)
    return chi <= dof + 6.0 * math.sqrt(2.0 * dof) + 12.0


def main():
    s = Solution([1, 2, 3])
    first = s.shuffle()
    print(f"example: shuffle is a permutation of [1, 2, 3] {b(same_values(first, [1, 2, 3]))}")
    print(f"reset gives [1, 2, 3] {b(s.reset() == [1, 2, 3])}")
    again = s.shuffle()
    print(f"shuffle again is a permutation {b(same_values(again, [1, 2, 3]))}")
    one = Solution([42])
    print(f"one element: {one.shuffle()[0]}")
    empty = Solution([])
    print(f"no elements: {len(empty.shuffle())}")
    dup = Solution([5, 5, 7, 7, 7])
    ok = True
    for _ in range(1000):
        ok = ok and same_values(dup.shuffle(), [5, 5, 7, 7, 7])
    print(f"repeated values: 1000 shuffles keep them {b(ok)}")
    print(f"3 elements, 60000 shuffles: all 6 orders equally likely {b(fair(3, 60000))}")
    print(f"4 elements, 48000 shuffles: all 24 orders equally likely {b(fair(4, 48000))}")
    print(f"5 elements, 60000 shuffles: all 120 orders equally likely {b(fair(5, 60000))}")
    big = Solution(list(range(50)))
    lands = [0] * 50
    for _ in range(20000):
        a = big.shuffle()
        for p in range(50):
            if a[p] == 0:
                lands[p] += 1
    chi = 0.0
    for p in range(50):
        d = lands[p] - 400.0
        chi += d * d / 400.0
    print(f"50 elements, 20000 shuffles: element 0 lands evenly {b(chi <= 49.0 + 6.0 * math.sqrt(98.0) + 12.0)}")
    print(f"reset after 20000 shuffles gives 0..49 {b(big.reset()[0] == 0 and big.reset()[49] == 49)}")


main()
