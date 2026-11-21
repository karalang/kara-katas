# LeetCode #2529: Maximum Count of Positive Integer and Negative Integer
# -- Python mirror of the ★ arm (count.kara): two binary searches, one for
# the first number not below 0 and one for the first above 0.


def first_where(nums, above):
    lo = 0
    hi = len(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > above:
            hi = mid
        else:
            lo = mid + 1
    return lo


def maximum_count(nums):
    negatives = first_where(nums, -1)
    positives = len(nums) - first_where(nums, 0)
    return max(negatives, positives)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    fixed = [
        [-2, -1, -1, 1, 2, 3],
        [-3, -2, -1, 0, 0, 1, 2],
        [5, 20, 66, 1314],
        [0],
        [-2000],
        [0, 0, 0, 2000],
        [-5, -4, 0, 0, 3, 4],
        [-1, -1, -1, -1, 1, 1, 1, 1],
    ]
    for nums in fixed:
        print(f"{show(nums)} -> {maximum_count(nums)}")
    seed = [2529]
    for count, most, top in [(3000, 40, 5), (1000, 2000, 2000)]:
        total = 0
        check = 0
        for _ in range(count):
            n = next_random(seed) % most + 1
            nums = sorted(next_random(seed) % (2 * top + 1) - top for _ in range(n))
            a = maximum_count(nums)
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"{count} random lists of up to {most} numbers within {top}: total {total}, checksum {check}")


main()
