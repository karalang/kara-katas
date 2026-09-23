"""LeetCode #321: Create Maximum Number — Python mirror of
create_max_number.kara.

Same algorithm (try every split, shrink each side with a monotonic stack,
merge on whole-suffix comparison), same demo cases, byte-identical output."""


def max_subsequence(nums: list[int], keep: int) -> list[int]:
    stack: list[int] = []
    drop = len(nums) - keep
    for d in nums:
        while drop > 0 and stack and stack[-1] < d:
            stack.pop()
            drop -= 1
        stack.append(d)
    while len(stack) > keep:
        stack.pop()
    return stack


def suffix_greater(a: list[int], i: int, b: list[int], j: int) -> bool:
    x, y = i, j
    while x < len(a) and y < len(b) and a[x] == b[y]:
        x += 1
        y += 1
    if y == len(b):
        return x < len(a)
    if x == len(a):
        return False
    return a[x] > b[y]


def merge(a: list[int], b: list[int]) -> list[int]:
    out = []
    i = j = 0
    while i < len(a) or j < len(b):
        if suffix_greater(a, i, b, j):
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out


def max_number(nums1: list[int], nums2: list[int], k: int) -> list[int]:
    m, n = len(nums1), len(nums2)
    best: list[int] = []
    for i in range(max(0, k - n), min(k, m) + 1):
        candidate = merge(max_subsequence(nums1, i), max_subsequence(nums2, k - i))
        if not best or suffix_greater(candidate, 0, best, 0):
            best = candidate
    return best


def show(v: list[int]) -> str:
    return "[" + ", ".join(str(d) for d in v) + "]"


def report(nums1: list[int], nums2: list[int], k: int) -> None:
    answer = max_number(nums1, nums2, k)
    print(f"{show(nums1)} {show(nums2)} k={k} -> {show(answer)}")


class Lcg:
    def __init__(self, seed: int) -> None:
        self.seed = seed

    def next(self) -> int:
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def digits(length: int, rng: Lcg) -> list[int]:
    return [rng.next() % 10 for _ in range(length)]


def main() -> None:
    report([3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5)
    report([6, 7], [6, 0, 4], 5)
    report([3, 9], [8, 9], 3)

    report([2, 5, 6, 4, 4, 0], [7, 3, 8, 0, 6, 5, 7, 6, 2], 15)
    report([6, 7, 6, 7, 6, 7, 0], [6, 7, 6, 7, 6, 7, 1], 14)
    report([8, 9, 9], [8, 9, 9, 1], 6)

    report([1, 2, 3], [4, 5], 0)
    report([], [1, 2, 3], 2)
    report([5, 4, 3], [], 3)
    report([1, 2], [3], 3)
    report([0, 0, 0], [0, 0], 4)
    report([9, 9], [9, 9, 9], 3)

    rng = Lcg(321)
    for length in [3, 5, 7]:
        a = digits(length, rng)
        b = digits(length + 1, rng)
        report(a, b, length + length // 2 + 1)

    for length in [20, 60, 150]:
        a = digits(length, rng)
        b = digits(length + 7, rng)
        k = length + length // 2
        answer = max_number(a, b, k)
        fold = 0
        for d in answer:
            fold = (fold * 131 + d + 1) % 1000000007
        print(f"m={length} n={length + 7} k={k} -> {len(answer)} digits, fold {fold}")

if __name__ == "__main__":
    main()
