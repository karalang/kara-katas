"""Benchmark mirror of LeetCode #321 — same split-shrink-merge as
bench/create_max_number.kara."""

LEN1 = 1500
LEN2 = 1700
PASSES = 24
MODULUS = 1073741789


class Lcg:
    def __init__(self, seed: int) -> None:
        self.seed = seed

    def next(self) -> int:
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def shrink(nums: list[int], keep: int, out: list[int]) -> None:
    top = 0
    drop = len(nums) - keep
    for d in nums:
        while drop > 0 and top > 0 and out[top - 1] < d:
            top -= 1
            drop -= 1
        if top < keep:
            out[top] = d
            top += 1
        else:
            drop -= 1


def suffix_greater(a: list[int], alen: int, i: int, b: list[int], blen: int, j: int) -> bool:
    x, y = i, j
    while x < alen and y < blen and a[x] == b[y]:
        x += 1
        y += 1
    if y == blen:
        return x < alen
    if x == alen:
        return False
    return a[x] > b[y]


def merge(a: list[int], alen: int, b: list[int], blen: int, out: list[int]) -> None:
    i = j = t = 0
    while i < alen or j < blen:
        if suffix_greater(a, alen, i, b, blen, j):
            out[t] = a[i]
            i += 1
        else:
            out[t] = b[j]
            j += 1
        t += 1


def main() -> None:
    rng = Lcg(321)
    sink = 0
    digits_out = 0

    left = [0] * (LEN1 + LEN2)
    right = [0] * (LEN1 + LEN2)
    cand = [0] * (LEN1 + LEN2)
    best = [0] * (LEN1 + LEN2)

    for p in range(PASSES):
        nums1 = [rng.next() % 10 for _ in range(LEN1)]
        nums2 = [rng.next() % 10 for _ in range(LEN2)]

        for k in (LEN1 // 3, (LEN1 + LEN2) // 2, LEN1 + LEN2 - 7 * (p + 1)):
            lo = max(0, k - LEN2)
            hi = min(k, LEN1)
            have = False
            for i in range(lo, hi + 1):
                shrink(nums1, i, left)
                shrink(nums2, k - i, right)
                merge(left, i, right, k - i, cand)
                if not have or suffix_greater(cand, k, 0, best, k, 0):
                    best[:k] = cand[:k]
                    have = True

            acc = 0
            for x in range(k):
                acc = (acc * 131 + best[x] + 1) % MODULUS
            sink = (sink * 1000003 + acc) % MODULUS
            digits_out += k

    print(f"sink {sink} digits {digits_out}")


if __name__ == "__main__":
    main()
